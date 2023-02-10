import json
import csv
import requests
import ensembl_rest
import re
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .models import Annotations, User, Genome, SequenceInfo, Discussion
from .forms.inscription_form import InscriptionForm
from .forms.database_form import DatabaseForm
from .forms.discussion_form import SendMessageForm, ViewMessageForm
from django.utils.safestring import mark_safe

## ---------------------------- Pour limiter l'accès aux pages ------------------------------------
# Role lecteur
def lecteur_required(user):
    if user.is_authenticated:
        return user.role == "lecteur"
    return False


# Role annotateur
def annotateur_required(user):
    if user.is_authenticated:
        return user.role == "annotateur"
    return False


# Role validateur
def validateur_required(user):
    if user.is_authenticated:
        return user.role == "validateur"
    return False


# Rôles validateur et annotateur
def a_v_role_required(user):
    if user.is_authenticated:
        return user.role in ["validateur", "annotateur"]
    return False


# Les 3 rôles
def role_required(user):
    if user.is_authenticated:
        return user.role in ["validateur", "annotateur", "lecteur"]
    return False


## -------------------------- PAGES D'ACCUEILS + INSCRIPTION CONNEXION  -----------------------------
## Page d'accueil du site Web
def annot_menu(request):
    return render(
        request,
        "genome/annot_menu.html",
        {
            "css_files": ["home_page.css"],
        },
    )


## Page d'inscription au site
def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Vérification que l'adresse email n'est pas déjà utilisée
            if User.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email", "Cette adresse email est déjà utilisée.")
            # Vérification que les mots de passe correspondent
            elif form.cleaned_data["password"] != request.POST.get("confirm_mdp"):
                form.add_error("password", "Les mots de passe ne correspondent pas.")
            else:
                # Validation du mot de passe avec validate_password
                try:
                    validate_password(form.cleaned_data["password"])
                except ValidationError as e:
                    form.add_error("password", e)
                    return render(
                        request,
                        "genome/inscription.html",
                        {"form": form, "css_files": ["Inscription.css"]},
                    )
                # Création d'un objet User
                user = User()
                user.username = form.cleaned_data["email"]
                user.email = form.cleaned_data["email"]
                user.numero_tel = form.cleaned_data["numero_tel"]
                user.nom = form.cleaned_data["nom"]
                user.prenom = form.cleaned_data["prenom"]
                user.role = form.cleaned_data["role"]
                # Cryptage du mot de passe pour le stocker dans la base de données
                user.set_password(form.cleaned_data["password"])
                # Enregistrement des données d'inscription dans la base de données
                user.save()
                messages.success(
                    request, "Votre inscription a été effectuée avec succès."
                )
                # Envoi d'un email de confirmation
                send_mail(
                    "Confirmation d'inscription",
                    "Merci de vous être inscrit sur notre site.",
                    "cypsgenome@gmail.com",
                    [user.email],
                    fail_silently=False,
                )
                # Redirection vers la page d'accueil du site
                return redirect("inscription")
    else:
        form = InscriptionForm()

    return render(
        request,
        "genome/inscription.html",
        {
            "form": form,
            "css_files": ["Inscription.css"],
        },
    )


## Page de connexion au site
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_validated == True:
                login(request, user)
                if user.role == "annotateur":
                    # Redirection vers une page pour les annotateurs
                    return redirect("annotateur_page")
                elif user.role == "lecteur":
                    # Redirection vers une page pour les lecteurs
                    return redirect("lecteur_page")
                elif user.role == "validateur":
                    # Redirection vers une page pour les validateurs
                    return redirect("validateur_page")
            elif user.is_validated == False:
                # Message d'erreur compte en cours de validation
                messages.error(
                    request, "Ton compte est en attente de validation par l'admin."
                )
        else:
            # Message d'erreur Email ou mot de passe incorect
            messages.error(request, "Email ou mot de passe incorect.")
    return render(
        request,
        "genome/login.html",
        {
            "css_files": ["login.css"],
        },
    )


# Pour se deconnecter
def logout_view(request):
    logout(request)
    return redirect("/")


# Page d'accueil des Annotateurs
@user_passes_test(annotateur_required, login_url="/login/")
def annotateur_page(request):
    return render(
        request,
        "genome/annotateur_page.html",
        {
            "css_files": ["form.css"],
        },
    )


# Page d'accueil des Validateurs
@user_passes_test(validateur_required, login_url="/login/")
def validateur_page(request):
    return render(
        request,
        "genome/validateur_page.html",
        {
            "css_files": ["form.css"],
        },
    )


# Page d'accueil des Lecteurs
@user_passes_test(lecteur_required, login_url="/login/")
def lecteur_page(request):
    return render(
        request,
        "genome/lecteur_page.html",
        {
            "css_files": ["form.css"],
        },
    )


## --------------------- BANQUES EXTERNES / ALIGNEMENT DE SEQUENCES (API) --------------------

def get_id_InterPro_from_Uniprot(id_databank) :

    url = f"https://rest.uniprot.org/uniprotkb/search?query={id_databank}"
    response = requests.get(url)
    #on récupère les infos qui nous interessent sous le format json
    response = response.json()

    dic = response['results'][0]['uniProtKBCrossReferences']
    for i in range(len(dic)) :
        if dic[i]['database'] == 'InterPro' : 
            id_Interpro = dic[i]['id']

    return id_Interpro


def get_data_from_InterPro(id_databank) :

    info = []
    go_terms= []

    #Appel de la fonction id_databank
    id_Interpro = get_id_InterPro_from_Uniprot(id_databank)

    url = f'https://www.ebi.ac.uk/interpro/api/entry/interpro/{id_Interpro}'
    response = requests.get(url)
    #on récupère les infos sous le format json
    response = response.json()

    info.append(response['metadata']['accession'])
    info.append(response['metadata']['entry_id'])
    info.append(response['metadata']['type'])

    #On met dans uen liste les infos go_terms contenu dans le json
    for go in range(len(response['metadata']['go_terms'])):
        go_terms.append(response['metadata']['go_terms'][go]['identifier'])
        go_terms.append(response['metadata']['go_terms'][go]['name'])
        go_terms.append(response['metadata']['go_terms'][go]['category']['code'])
        go_terms.append(response['metadata']['go_terms'][go]['category']['name'])

    grouped_data = []
    temp = []

    #On fait une liste de liste regroupant les go_terms et leurs infos
    for i, item in enumerate(go_terms):
        if isinstance(item, str) and item.startswith('GO'):
            if temp:
                grouped_data.append(temp)
            temp.append(item)
            temp.extend(go_terms[i+1:i+4])
            grouped_data.append(temp)
            temp = []

    # Pour faciliter l'affichage dans le HTML
    grouped_data = [{'identifiant': ele[0],
        'nom': ele[1],
        'categorie_code': ele[2],
        'categorie_nom': ele[3],}
    for ele in grouped_data]   

    return info, grouped_data


def get_data_from_ensembl(id_databank):

    result = ensembl_rest.sequence_id(id_databank, content_type="application/json")

    return result


def get_data_from_uniprot(id_databank):

    info = []
    url = f"https://rest.uniprot.org/uniprotkb/search?query={id_databank}"

    response = requests.get(url)

    #on récupère les infos qui nous interessent sous le format json
    response = response.json()
    dic = response['results'][0]

    #On récupère les infos et on les met dans une liste
    if 'uniProtkbId' in dic : 
        uniProtkbId = dic['uniProtkbId'] 
        info.append(uniProtkbId)

    else :
        info.append('None')
   
    if 'scientificName' in dic['organism'] :
        espece = dic['organism']['scientificName']
        info.append(espece)
        
    else :
        info.append('None')

    if 'alternativeNames' in dic['proteinDescription'] : 
        fonction = dic['proteinDescription']['alternativeNames'][0]['fullName']['value']
        info.append(fonction)

    else :
        info.append('None')

    if 'geneName' in dic['genes'][0] :
        gene_symbol = dic['genes'][0]['geneName']['value']
        info.append(gene_symbol)

    else :
        info.append('None')

    if 'recommendedName' in dic['proteinDescription'] : 
        fonction = response['results'][0]['proteinDescription']['recommendedName']['fullName']['value']
        info.append(fonction)

    else :
        info.append('None')
        
    if 'orderedLocusNames' in dic['genes'][0] : 
        gene_name = response['results'][0]['genes'][0]['orderedLocusNames'][0]['value']
        info.append(gene_name)

    else :
        info.append('None')

    if 'length' in dic['sequence'] : 
        longueur = dic['sequence']['length']
        info.append(longueur)
    
    else :
        info.append('None')

    return info


## Page des banques externes
@user_passes_test(role_required, login_url="/login/")
def show_sequences(request):
    #On montre les infos dans les differentes banques de données

    if request.method == "GET":

        form = DatabaseForm()

        return render(request, 'genome/select_database.html', {'form': form})

    elif request.method == 'POST':

        form = DatabaseForm(request.POST)

        if form.is_valid():

            selected_database = form.cleaned_data['Choisir_une_banque_de_données_externe']
            id_databank = form.cleaned_data['id_databank']

            if selected_database == 'InterPro':

                info, go_terms = get_data_from_InterPro(id_databank)

                return render(request, "genome/result_InterPro.html", {'selected_database': selected_database, 'inter': info, 'go': go_terms})

            elif selected_database == 'Ensembl':

                data = get_data_from_ensembl(id_databank)

                return render(request, "genome/result_ensembl.html", {'selected_database': selected_database, 'results': data})

            elif selected_database == 'Uniprot':

                data = get_data_from_uniprot(id_databank)

                return render(request, 'genome/result_uniprot.html', {'results': data})
            
            return render(request, "genome/data.html", {'selected_database': selected_database, 'data': data})


## Comparaison et Alignement de séquences
@user_passes_test(role_required, login_url="/login/")
def blast_view(request):

    # Pour la liste déroulante
    sequences = SequenceInfo.objects.all()

    if request.method == "POST":
        seq_id = request.POST.get("seq_id")
        seq_type = request.POST.get("type_seq")
        sequence = SequenceInfo.objects.filter(seq_id=seq_id).first()

        if sequence:
            if seq_type == "pep":
                # On effectue la requête BLAST pour une recherche protéique
                sequence = sequence.seq_pep
                blast_result = NCBIWWW.qblast("blastp", "nr", sequence)
            elif seq_type == "cds":
                sequence = sequence.seq_cds
                # On effectue la requête BLAST pour une recherche nucléotidique
                blast_result = NCBIWWW.qblast("blastn", "nr", sequence)

            # On parse le fichier xml
            blast_records = NCBIXML.parse(blast_result)
            alignments = []

            # on stocke les infos importantes
            alignments = [
                {
                    "hit_id": alignment.hit_id,
                    "hit_def": alignment.hit_def,
                    "score": hsp.score,
                    "evalue": hsp.expect,
                    "identity": hsp.identities / hsp.align_length * 100,
                }
                for blast_record in blast_records
                for alignment in blast_record.alignments
                for hsp in alignment.hsps
            ]

            # on retourne les résultats dans notre fichier html
            return render(request, "genome/results.html", {"results": alignments})

        else:
            return HttpResponse("Aucune séquence trouvée avec l'ID: " + seq_id)

    else:
        return render(request, "genome/blast.html", {"sequences": sequences})


## ------------------------------------- GENOMES / GENES ------------------------------------
## Page pour chercher un génome ou un gène / une protéine dans la base de données du site
@user_passes_test(role_required, login_url="/login/")
def formulaire_genome(request):
    if request.method == 'GET':
        return render(request, 'genome/formulaire.html', {
        'css_files': ['formulaire.css'],
        })
    elif request.method == 'POST':
        accessionnb = request.POST.get('accessionnb')
        idsequence = request.POST.get('idsequence')
        espece = request.POST.get('espece')
        taille_min = request.POST.get('taille_min')
        taille_max = request.POST.get('taille_max')
        type_adn = request.POST.get('type_adn')
        seq_start = request.POST.get('seq_start')
        seq_end = request.POST.get('seq_end')
        strand = request.POST.get('strand')
        seq = request.POST.get('sequence')
        gene_biotype = request.POST.get('gene_biotype')
        output_type = request.POST.get('output_type')
        annotated_state = request.POST.get('annotated_state')
        if output_type == 'genome':
            query_params = {}
            if accessionnb:
                query_params["num_accession"] = accessionnb
            if espece:
                query_params['espece'] = espece
            if taille_min:
                query_params['longueur__gte'] = taille_min
            if taille_max:
                query_params['longueur__lte'] = taille_max
            if type_adn:
                query_params['type_adn'] = type_adn
            if annotated_state :
                query_params['annotated_genome'] = annotated_state
            if seq:
                seq = seq.replace("\r","")
                seq = seq.replace("\n","")
                if re.search("^[ATGC%]+$", seq) != None :
                    # regex %
                    if re.search("^[ATGC]+%$",seq):
                        #commence par seq
                        query_params['sequence__regex'] = "^" + seq.replace("%",".*")
                    elif re.search("%[ATGC]+$",seq) :
                        # se termine par seq
                        query_params['sequence__regex'] = seq.replace("%",".*") + "$"
                    elif re.search("%[ATGC]+%",seq) :
                        # contient seq
                        query_params['sequence__contains'] = seq.replace("%","")
                    elif re.search("^[A-Z]+$", seq) :
                        #egalite
                        query_params['sequence'] = seq
                else :
                    # valeurs aberrantes
                    query_params['sequence'] = None
            genomes = Genome.objects.filter(**query_params)
            return render(request, 'genome/genome_info.html', {'genomes': genomes})

        elif output_type == 'gene_protein':
            query_params = {}
            if accessionnb:
                query_params["num_accession"] = accessionnb
            if idsequence:
                query_params["seq_id"] = idsequence
            if seq_start:
                query_params["seq_start__gte"] = seq_start
            if seq_end:
                query_params["seq_end__lte"] = seq_end
            if strand:
                query_params["strand"] = strand
            if type_adn:
                query_params['type_adn'] = type_adn
            if taille_min:
                query_params['longueur__gte'] = taille_min
            if taille_max:
                query_params['longueur__lte'] = taille_max
            if gene_biotype:
                query_params['seq_biotype'] = gene_biotype
            if annotated_state :
                query_params['annotated_state'] = annotated_state
            if seq:
                if re.search("^[ATGC%]+$", seq) != None :
                    # sequence cds
                    if re.search("^[ATGC]+%$",seq):
                        #commence par seq
                        query_params['seq_cds__regex'] = "^" + seq.replace("%",".*")
                    elif re.search("%[ATGC]+$",seq) :
                        # se termine par seq
                        query_params['seq_cds__regex'] = seq.replace("%",".*") + "$"
                    elif re.search("%[ATGC]+%",seq) :
                        # contient seq
                        query_params['seq_cds__contains'] = seq.replace("%","")
                    elif re.search("^[ATGC]+$", seq) :
                        # égalité
                        query_params['seq_cds'] = seq
                elif re.search("^[A-Z%]+$", seq) != None :
                    # sequence pep
                    if re.search("^[A-Z]+%$",seq):
                        # commence par seq
                        query_params['seq_pep__regex'] = "^" + seq.replace("%",".*")
                    elif re.search("%[A-Z]+$",seq) :
                        # finit par seq
                        query_params['seq_pep__regex'] = seq.replace("%",".*") + "$"
                    elif re.search("%[A-Z]+%",seq) :
                        # contient seq
                        query_params['seq_pep__contains']= seq.replace("%","")
                    elif re.search("^[A-Z]+$", seq) :
                        # égalité
                        query_params['seq_pep'] = seq
                else :
                    # valeurs aberrantes
                    query_params['seq_cds'] = None
                    query_params['seq_pep'] = None  
            print(query_params)
            sequences = SequenceInfo.objects.filter(**query_params)
            return render(
                request, "genome/gene_protein_info.html", {"sequences": sequences}
            )


## Page de visualisation de la séquence du génome + les gènes associés
@user_passes_test(role_required, login_url="/login/")
def view_sequence(request):
    # Récupération de la séquence depuis le numéro accession fourni par l'url
    if request.method == "GET":
        numacc = request.GET.get("numacc")
        genome = Genome.objects.get(num_accession=numacc)
        sequence = genome.sequence
        genes = SequenceInfo.objects.filter(num_accession=numacc)
        # Bouton pour télécharger la séquence en .txt
        if request.GET.get("download"):
            response = HttpResponse(genome.sequence, content_type="text/plain")
            response["Content-Disposition"] = 'attachment; filename="{}.txt"'.format(
                genome.num_accession
            )
            return response
        return render(
            request,
            "genome/view_sequence.html",
            {
                "css_files": ["view_seq.css"],
                "numacc": numacc,
                "sequence": sequence,
                "genes": genes,
            },
        )


## Page de visualisation de gènes
@user_passes_test(role_required, login_url="/login/")
def view_genesequence(request):
    if request.method == "GET":
        seqid = request.GET.get('seqid')
        gene = SequenceInfo.objects.get(seq_id=seqid)
        nom = gene.seq_name
        genome = Genome.objects.get(num_accession = gene.num_accession)
        sequence_cds = gene.seq_cds
        sequence_pep = gene.seq_pep
        start = max(gene.seq_start - 1000, 0)
        end = min(gene.seq_end + 1000, genome.longueur)
        sequence_genome = genome.sequence[start:end]

        if start == 0 : 
            print('ok')
            sequence_genome = mark_safe( "<strong> <span style='color: orange ;'> 1 </span> </strong>" + sequence_genome.replace(sequence_cds, "<strong> <span style='color:green;'>" 
                    + str(gene.seq_start) + "</span> </strong>" + " " + "<span style='color:red;'>" + sequence_cds + "</span>" + 
                " " + "<strong>  <span style='color:green;'>" + str(gene.seq_end) + "</span> </strong>") + " <strong> <span style='color: orange ;'> ... -" + str(genome.longueur) + "</span> </strong>")

        elif end == genome.longueur : 
            sequence_genome = mark_safe("<strong> <span style='color: orange ;'> 1- ... </span> </strong>" + sequence_genome.replace(sequence_cds, 
                "<strong> <span style='color:green;'>" + str(gene.seq_start) + "</span> </strong>" + " " + "<span style='color:red;'>" + sequence_cds + "</span>" + 
                " " + "<strong>  <span style='color:green;'>" + str(gene.seq_end) + "</span> </strong>" ) + " <strong> <span style='color: orange ;'>" + str(genome.longueur) + "</span> </strong>")

        else : 
            sequence_genome = mark_safe("<strong> <span style='color: orange ;'> 1- ... </span> </strong>"+ sequence_genome.replace(sequence_cds,
                "<strong> <span style='color:green;'>" + str(gene.seq_start) + "</span> </strong>" + " " + "<span style='color:red;'>" + sequence_cds + "</span>" + 
                " " + "<strong>  <span style='color:green;'>" + str(gene.seq_end) + "</span> </strong>" ) + " <strong> <span style='color: orange ;'> ... -" + str(genome.longueur) + "</span> </strong>")



        download_type = request.GET.get("download")
        if download_type == "cds":
            response = HttpResponse(sequence_cds, content_type="text/plain")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="{}_cds.txt"'.format(gene.seq_id)
            return response
        elif download_type == "pep":
            response = HttpResponse(sequence_pep, content_type="text/plain")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="{}_pep.txt"'.format(gene.seq_id)
            return response
        return render(
            request,
            "genome/view_genesequence.html",
            {
                "css_files": ["view_seq.css"],
                "nom": nom,
                "sequence_cds": sequence_cds,
                "sequence_pep": sequence_pep,
                "seqid": seqid,
                "sequence_genome" : sequence_genome,
            },
        )


## Extracttion d'une séquence et de ses champs dans un txt
@user_passes_test(role_required, login_url="/login/")
def extract_data(request):
    if request.method == "GET":
        sequences = SequenceInfo.objects.filter(annotated_state__in=["annoté"])
        context = {"sequences": sequences}
        return render(request, "genome/search_sequence_info.html", context)

    if request.method == "POST":
        seq = SequenceInfo.objects.get(seq_id=request.POST.get("sequence"))
        fields = request.POST.getlist("fields")
        header = []
        row = []
        print(fields)
        if "num_accession" in fields:
            header.append("num_accession")
            row.append(seq.num_accession)
        if "seq_id" in fields:
            header.append("seq_id")
            row.append(seq.seq_id)
        if "type_adn" in fields:
            header.append("type_adn")
            row.append(seq.type_adn)
        if "seq_cds" in fields:
            header.append("seq_cds")
            row.append(seq.seq_cds)
        if "seq_pep" in fields:
            header.append("seq_pep")
            row.append(seq.seq_pep)
        if "seq_biotype" in fields:
            header.append("seq_biotype")
            row.append(seq.seq_biotype)
        if "longueur" in fields:
            header.append("longueur")
            row.append(seq.longueur)
        if "strand" in fields:
            header.append("strand")
            row.append(seq.strand)
        if "seq_start" in fields:
            header.append("seq_start")
            row.append(seq.seq_start)
        if "seq_end" in fields:
            header.append("seq_end")
            row.append(seq.seq_end)
        if "description" in fields:
            header.append("description")
            row.append(seq.description)

        with open("annotated_data.txt", "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            writer.writerow(row)

        sequences = SequenceInfo.objects.filter(annotated_state__in=["annoté"])

        message = "Les données ont été extraites avec succès."
        context = {"sequences": sequences, "message": message}
        return render(request, "genome/search_sequence_info.html", context)


## ------------------------------------- ANNOTATIONS ------------------------------------
## Page d'attribution d'une séquence à un annotateur
@user_passes_test(validateur_required, login_url="/login/")
def assign_annotation(request):
    if request.method == "GET":
        users = User.objects.filter(role__in=["annotateur", "validateur"])
        genomes = Genome.objects.filter(annotated_genome__in=["non annoté"])
        sequences = SequenceInfo.objects.exclude(
            annotations__annotation_status__in=["attribué", "en cours", "validé"]
        ).filter(annotated_state__in=["non annoté"])
        context = {
            "users": users,
            "genomes": genomes,
            "sequences": sequences,
            "message": "",
        }
        return render(request, "genome/assign_annotation.html", context)

    if request.method == "POST":
        email = request.POST.get("user")
        sequence_id = request.POST.get("sequence")
        user = User.objects.get(email=email)
        sequence = SequenceInfo.objects.get(seq_id=sequence_id)
        genome = Genome.objects.get(num_accession=sequence.num_accession)
        annotation = Annotations.objects.create(
            email_annot=user,
            sequence_id=sequence,
            genome_ID=genome,
            annotation_status="attribué",
        )
        annotation.save()
        send_mail(
            "Attribution d'une séquence à annoter",
            "Vous avez une nouvelle séquence à annoter ! Son ID est : ("
            + sequence_id
            + ")",
            "cypsagenome@gmail.com",
            [email],
            fail_silently=False,
        )
        message = "La séquence '{}' a été attribuée à '{}'".format(
            sequence_id, user.email
        )
        context = {
            "users": User.objects.filter(role__in=["annotateur", "validateur"]),
            "genomes": Genome.objects.filter(annotated_genome__in=["non annoté"]),
            "sequences": SequenceInfo.objects.exclude(
                annotations__annotation_status__in=["attribué", "en cours", "validé"]
            ).filter(annotated_state__in=["non annoté"]),
            "message": message,
        }
        return render(request, "genome/assign_annotation.html", context)


## Page de vaidation ou non des annotations
@user_passes_test(validateur_required, login_url="/login/")
def validate_annotation(request):
    if request.method == "GET":
        annotations = Annotations.objects.filter(annotation_status="en cours")
        return render(request, "genome/validation.html", {"annotations": annotations})
    elif request.method == "POST":
        count_validated = 0
        count_rejected = 0
        for annot in Annotations.objects.filter(annotation_status="en cours"):
            if request.POST.get("validate_reject-" + str(annot.annot_id)) == "validate":
                annot.annotation_status = "validé"
                annot.comments = request.POST.get("comment-" + str(annot.annot_id))
                annot.save()
                id = annot.sequence_id.seq_id
                seq = SequenceInfo.objects.get(seq_id=id)
                seq.seq_name = annot.seq_name
                seq.seq_biotype = annot.seq_biotype
                seq.strand = annot.strand
                seq.description = annot.description
                seq.annotated_state = "annoté"
                seq.save()
                
                count_validated += 1
                send_mail(
                    "Annotation Validée",
                    "Votre annotation de la séquence ("
                    + str(annot.sequence_id.seq_id)
                    + ") a été validée avec le commentaire suivant : "
                    + annot.comments,
                    "cypsgenome@gmail.com",
                    [annot.email_annot],
                    fail_silently=False,
                )
            elif request.POST.get("validate_reject-" + str(annot.annot_id)) == "reject":
                annot.annotation_status = "rejeté"
                annot.comments = request.POST.get("comment-" + str(annot.annot_id))
                annot.save()
                count_rejected += 1
                send_mail(
                    "Annotation Rejetée",
                    "Votre annotation ID ("
                    + str(annot.sequence_id.seq_id)
                    + ") a été rejetée avec le commentaire suivant : "
                    + annot.comments,
                    "cypsgenome@gmail.com",
                    [annot.email_annot],
                    fail_silently=False,
                )
        message = ""
        if count_validated == 1:
            message += str(count_validated) + " annotation a été validée. "
        if count_rejected == 1:
            message += str(count_rejected) + " annotation a été rejetée. "
        if count_validated > 1:
            message += str(count_validated) + " annotations ont été validées. "
        if count_rejected > 1:
            message += str(count_rejected) + " annotations ont été rejetées. "
        context = {"message": message}
        return render(request, "genome/success.html", context)


## Page des annotations attribuées
@user_passes_test(a_v_role_required, login_url="/login/")
def annotations(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            email = request.user.email
            annotations = Annotations.objects.filter(
                email_annot__email=email, annotation_status="attribué"
            )
            if annotations:
                context = {"annotations": annotations}
                return render(request, "genome/annotations.html", context)
            else:
                context = {"message": "Aucune séquence n'a été attribuée"}
                return render(request, "genome/annotations.html", context)
        else:
            return redirect("login")


## Formulaire de d'annotation
@user_passes_test(a_v_role_required, login_url="/login/")
def formulaire_annotation(request, annotation_id):
    if request.method == "GET":
        annotation = Annotations.objects.filter(annot_id=annotation_id)[0]
        if request.user.email == annotation.email_annot.email:
            context = {"annotation": annotation}
            return render(request, "genome/formulaire_annotation.html", context)
        else:
            return redirect("login")
    if request.method == "POST":
        sens = request.POST.get("Brin")
        seq_biotype = request.POST.get("biotype")
        description = request.POST.get("description")
        seq_name = request.POST.get("seq_name")
        annot = Annotations.objects.get(annot_id=annotation_id)
        annot.seq_biotype = seq_biotype
        annot.strand = sens
        annot.description = description
        annot.seq_name = seq_name
        annot.annotation_status = "en cours"
        annot.save()
        message = "L'annotation pour la séquence '{}' a bien été enregistrée. Un validateur va analyser cette anotations.".format(
            annot.sequence_id.seq_id
        )
        context = {"message": message}
        return render(request, "genome/success.html", context)


## Page de toutes les annotations en cours
@user_passes_test(role_required, login_url="/login/")
def annotation_list(request):
    # Récupérer toutes les annotations en attente de validation de génome de la base de données
    query_param = {}
    query_param["annotation_status"] = "en cours"
    annotations = Annotations.objects.filter(**query_param)
    # Rendre le template avec le contexte de données
    return render(request, "genome/annotation_list.html", {"annotations": annotations})

## Forum des annotateurs (et validateurs)
@user_passes_test(a_v_role_required, login_url="/login/")
def send_message(request):
    if request.method == "GET":
        messages = Discussion.objects.filter(Q(envoyeur=request.user) | Q(destinataire=request.user)).order_by('timestamp')
        return render(request, 'genome/view_discussion.html', {'messages': messages})
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            destinataire = form.cleaned_data['destinataire']
            message = form.cleaned_data['message']
            Discussion.objects.create(envoyeur=request.user, destinataire=destinataire, message=message)
            mess ="Ton message a bien été envoyé à " + str(destinataire) + "."
            return render(request, 'genome/send_message.html', {'form': form, 'mess':mess})
    else:
        form = SendMessageForm()
    return render(request, 'genome/send_message.html', {'form': form})
