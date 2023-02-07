from django.shortcuts import render, redirect, get_object_or_404
from .models import Annotations, User, Genome, SequenceInfo
from .forms.inscription_form import InscriptionForm
from .forms.database_form import DatabaseForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
import urllib.request
import re
from django.http import HttpResponse
import urllib.request
import requests
import ensembl_rest
import json
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML




# Page d'accueil du site Web
def annot_menu(request):
    return render(request, 'genome/annot_menu.html', {
        'css_files': ['home_page.css'],
    })

# Page d'inscription au site
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Vérification que l'adresse email n'est pas déjà utilisée
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'Cette adresse email est déjà utilisée.')
            # Vérification que les mots de passe correspondent
            elif form.cleaned_data['password'] != request.POST.get('confirm_mdp'):
                form.add_error('password', 'Les mots de passe ne correspondent pas.')
            else:
                # Validation du mot de passe avec validate_password
                try:
                    validate_password(form.cleaned_data['password'])
                except ValidationError as e:
                    form.add_error('password', e)
                    return render(request, 'genome/inscription.html', {'form': form, 'css_files': ['Inscription.css']})
                # Création d'un objet User
                user = User()
                user.username = form.cleaned_data['email']
                user.email = form.cleaned_data['email']
                user.numero_tel = form.cleaned_data['numero_tel']
                user.nom = form.cleaned_data['nom']
                user.prenom = form.cleaned_data['prenom']
                user.role= form.cleaned_data['role']
                # Cryptage du mot de passe pour le stocker dans la base de données
                user.set_password(form.cleaned_data['password'])
                # Enregistrement des données d'inscription dans la base de données
                user.save()
                messages.success(request, "Votre inscription a été effectuée avec succès.")
                # Envoi d'un email de confirmation
                send_mail(
                    'Confirmation d\'inscription',
                    'Merci de vous être inscrit sur notre site.',
                    'cypsgenome@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                # Redirection vers la page d'accueil du site
                return redirect('inscription')
    else:
        form = InscriptionForm()

    return render(request, 'genome/inscription.html', {
        'form': form,
        'css_files': ['Inscription.css'],
    })

# Page de toutes les annotations en cours
def annotation_list(request):
    # Récupérer toutes les annotations en attente de validation de génome de la base de données
    query_param={}
    query_param['annotation_status'] = 'en cours'
    annotations = Annotations.objects.filter(**query_param)
    # Rendre le template avec le contexte de données
    return render(request, 'genome/annotation_list.html',{'annotations': annotations})

# Page de connexion au site 
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None :
            if user.is_validated == True:
                login(request, user)
                if user.role == "annotateur":
                    # Redirection vers une page pour les annotateurs
                    return redirect('annotateur_page')
                elif user.role == "lecteur":
                    # Redirection vers une page pour les lecteurs
                    return redirect('lecteur_page')
                elif user.role == "validateur":
                    # Redirection vers une page pour les validateurs
                    return redirect('validateur_page')
            elif user.is_validated == False:
                # Message d'erreur compte en cours de validation
                messages.error(request, "Ton compte est en attente de validation par l'admin.")
        else:
            # Message d'erreur Email ou mot de passe incorect
                messages.error(request, "Email ou mot de passe incorect.")
    return render(request, 'genome/login.html', {
        'css_files': ['login.css'],
    })

# Pour se deconnecter 
def logout_view(request):
    logout(request)
    return redirect('/')

# Page d'accueil des Annotateurs
def annotateur_required(user):
    if user.is_authenticated:
        return user.role == "annotateur"
    return False

@user_passes_test(annotateur_required, login_url='/login/')
def annotateur_page(request):
    return render(request, 'genome/annotateur_page.html', {
        'css_files': ['form.css'],
    })

# Page d'accueil des Validateurs
def validateur_required(user):
    if user.is_authenticated:
        return user.role == "validateur"
    return False

@user_passes_test(validateur_required, login_url='/login/')
def validateur_page(request):
    return render(request, 'genome/validateur_page.html', {
        'css_files': ['form.css'],
    })

# Page d'accueil des Lecteurs
def lecteur_required(user):
    if user.is_authenticated:
        return user.role == "lecteur"
    return False

@user_passes_test(lecteur_required, login_url='/login/')
def lecteur_page(request):
    return render(request, 'genome/lecteur_page.html', {
        'css_files': ['form.css'],
    })

# Page de vaidation ou non des annotations
@user_passes_test(validateur_required, login_url='/login/')
def validate_annotation(request):
    if request.method == "GET":
        annotations = Annotations.objects.filter(annotation_status='en cours')
        return render(request, 'genome/validation.html', {'annotations': annotations})
    elif request.method == "POST":
        count_validated = 0
        count_rejected = 0
        for annot in Annotations.objects.filter(annotation_status='en cours'):
            if request.POST.get('validate_reject-' + str(annot.annot_id)) == 'validate':
                annot.annotation_status = 'validé'
                annot.comments = request.POST.get('comment-' + str(annot.annot_id))
                annot.save()
                count_validated += 1
                send_mail(
                    'Annotation Validée',
                    'Votre annotation de la séquence ('+str(annot.sequence_id.seq_id)+') a été validée avec le commentaire suivant : ' + annot.comments,
                    'cypsgenome@gmail.com',
                    [annot.email_annot],
                    fail_silently=False,
                )
            elif request.POST.get('validate_reject-' + str(annot.annot_id)) == 'reject':
                annot.annotation_status = 'rejeté'
                annot.comments = request.POST.get('comment-' + str(annot.annot_id))
                annot.save()
                count_rejected += 1
                send_mail(
                    'Annotation Rejetée',
                    'Votre annotation ID ('+str(annot.sequence_id.seq_id)+') a été rejetée avec le commentaire suivant : ' + annot.comments,
                    'cypsgenome@gmail.com',
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
        context = {'message': message}
        return render(request,"genome/success.html", context)


# Les 3 rôles
def role_required(user):
    if user.is_authenticated:
        return user.role in ['validateur', 'annotateur', 'lecteur']
    return False

# Page pour accéder aux banques externes
def get_data_from_ncbi(id_databank):
    url = f'https://api.ncbi.nlm.nih.gov/data/databank/id/{id_databank}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_data_from_ensembl(id_databank):
    result = ensembl_rest.sequence_id(id_databank, content_type='application/json')
    return result

def get_data_from_uniprot(id_databank):
    url = f'https://www.uniprot.org/uniprot/{id_databank}.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None



def show_sequences(request):
    if request.method == "GET":
        form = DatabaseForm()
        return render(request, 'genome/select_database.html', {'form': form})
    elif request.method == 'POST':
        form = DatabaseForm(request.POST)
        if form.is_valid():
            selected_database = form.cleaned_data['Choisir_une_banque_de_données_externe']
            id_databank = form.cleaned_data['id_databank']
            if selected_database == 'NCBI':
                data = get_data_from_ncbi(id_databank)
            elif selected_database == 'Ensembl':
                data = get_data_from_ensembl(id_databank)
            elif selected_database == 'Uniprot':
                data = get_data_from_uniprot(id_databank)
            data=json.dumps(data, indent=4)
            return render(request, "genome/data.html", {'selected_database': selected_database, 'data': data})


# Pour chercher un génome ou un gène / une protéine dans la base de données du site
@user_passes_test(role_required, login_url='/login/')

def formulaire_genome(request):
    if request.method == 'GET':
        return render(request, 'genome/formulaire.html', {
        'css_files': ['form.css'],
        })
    elif request.method == 'POST':
        accessionnb = request.POST.get('accessionnb')
        espece = request.POST.get('espece')
        souche = request.POST.get('souche')
        taille_seq = request.POST.get('taille_seq')
        idsequence = request.POST.get('idsequence')
        type_adn = request.POST.get('type_adn')
        seq_start = request.POST.get('seq_start')
        seq_end = request.POST.get('seq_end')
        strand = request.POST.get('strand')
        seq = request.POST.get('sequence')
        seq_taille = request.POST.get('seq_taille')
        gene_biotype = request.POST.get('gene_biotype')
        output_type = request.POST.get('output_type')
        if output_type == 'genome':
            query_params = {}
            if accessionnb:
                query_params['num_accession'] = accessionnb
            if espece:
                query_params['espece'] = espece
            if souche:
                query_params['souche'] = souche
            if taille_seq:
                query_params['longueur'] = taille_seq
            if type_adn:
                query_params['type_adn'] = type_adn
            if seq:
                query_params['sequence'] = seq
            query_params['annotated_genome']='annoté'
            genomes = Genome.objects.filter(**query_params)
            return render(request, 'genome/genome_info.html', {'genomes': genomes})
        elif output_type == 'gene_protein':
            query_params = {}
            if accessionnb:
                query_params['num_accession'] = accessionnb
            if idsequence:
                query_params['seq_id'] = idsequence
            if seq_start:
                query_params['seq_start'] = seq_start
            if seq_end:
                query_params['seq_end'] = seq_end
            if strand :
                query_params['strand'] = strand
            if type_adn:
                query_params['type_adn'] = type_adn
            if seq:
                query_params['sequence'] = seq
            if seq_taille:
                query_params['longueur'] = taille_seq
            if gene_biotype:
                query_params['seq_biotype'] = gene_biotype
            query_params['annotated_state'] = 'annoté'
            print(query_params)
            sequences = SequenceInfo.objects.filter(**query_params)
            return render(request, 'genome/gene_protein_info.html', {'sequences': sequences})
            
def view_sequence(request): 
    ## Visualisation de la séquence du génome + les gènes associés
    # Récupération de la séquence depuis le numéro accession fourni par l'url
    if request.method == "GET":
        numacc = request.GET.get('numacc')
        genome = Genome.objects.get(num_accession=numacc,annotated_genome='annoté')
        sequence = genome.sequence
        genes = SequenceInfo.objects.filter(num_accession=numacc)
        # Bouton pour télécharger la séquence en .txt
        if request.GET.get('download'):
                response = HttpResponse(genome.sequence, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(genome.num_accession)
                return response
        return render(request,"genome/view_sequence.html",{'css_files': ['view_seq.css'],
        'numacc': numacc,
        'sequence': sequence,
        'genes': genes})

def view_genesequence(request):
    ## Genes
    if request.method == "GET":
        seqid = request.GET.get('seqid')
        gene = SequenceInfo.objects.get(seq_id=seqid,annotated_state='annoté')
        nom = gene.seq_name
        sequence_cds = gene.seq_cds
        sequence_pep = gene.seq_pep
        download_type = request.GET.get('download')
        if download_type == 'cds':
                response = HttpResponse(sequence_cds, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="{}_cds.txt"'.format(gene.seq_id)
                return response
        elif download_type == 'pep':
                response = HttpResponse(sequence_pep, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="{}_pep.txt"'.format(gene.seq_id)
                return response
        return render(request,"genome/view_genesequence.html",{'css_files': ['view_seq.css'],
        'nom':nom,
        'sequence_cds': sequence_cds,
        'sequence_pep': sequence_pep,
        'seqid': seqid})
        
## Page d'attribution d'une séquence à un annotateur
@user_passes_test(validateur_required, login_url='/login/')
def assign_annotation(request):
    if request.method == 'GET':
        users = User.objects.filter(role__in=['annotateur', 'validateur'])
        genomes = Genome.objects.filter(annotated_genome__in=['non annoté'])
        sequences = SequenceInfo.objects.exclude(annotations__annotation_status__in=['attribué', 'en cours', 'validé']).filter(annotated_state__in=['non annoté'])
        context = {'users': users, 'genomes': genomes, 'sequences': sequences, 'message': ''}
        return render(request, 'genome/assign_annotation.html', context)

    if request.method == 'POST':
        email = request.POST.get('user')
        sequence_id = request.POST.get('sequence')
        user = User.objects.get(email=email)
        sequence = SequenceInfo.objects.get(seq_id=sequence_id)
        genome = Genome.objects.get(num_accession=sequence.num_accession)
        annotation = Annotations.objects.create(email_annot=user, sequence_id=sequence, genome_ID=genome, annotation_status='attribué')
        annotation.save()
        send_mail("Attribution d'une séquence à annoter",
                    'Vous avez une nouvelle séquence à annoter ! Son ID est : ('+sequence_id+')',
                    'cypsagenome@gmail.com',
                    [email],
                    fail_silently=False,
                )
        message = "La séquence '{}' a été attribuée à '{}'".format(sequence_id, user.email)
        context = {'users': User.objects.filter(role__in=['annotateur', 'validateur']),'genomes':Genome.objects.filter(annotated_genome__in=['non annoté']), 'sequences': SequenceInfo.objects.exclude(annotations__annotation_status__in=['attribué', 'en cours', 'validé']).filter(annotated_state__in=['non annoté']), 'message': message}
        return render(request, 'genome/assign_annotation.html',context)


def blast_view(request):

    sequences = SequenceInfo.objects.all()
    #print(sequences)
    if request.method == 'POST':
        
        seq_id = request.POST.get('seq_id')
        seq_type = request.POST.get('type_seq')
        #print(request.POST)
        sequence = SequenceInfo.objects.filter(seq_id=seq_id).first()
        

        if sequence:
            if seq_type == "pep":
                sequence = sequence.seq_pep
            elif seq_type == "cds":
                sequence = sequence.seq_cds
            
            # Effectuer la requête BLAST
            blast_result = NCBIWWW.qblast("blastp", "nr", sequence)
            #print(blast_result)
            
            # Analyser les résultats BLAST
            blast_records = NCBIXML.parse(blast_result)
            #print(blast_records)
            alignments = []
            alignments = [{'hit_id': alignment.hit_id,
               'hit_def': alignment.hit_def,
               'score': hsp.score,
               'evalue': hsp.expect,
               'identity': hsp.identities / hsp.align_length * 100}
              for blast_record in blast_records
              for alignment in blast_record.alignments
              for hsp in alignment.hsps]
                

            return render(request, 'genome/results.html', {'results': alignments})
        else:
            return HttpResponse('Aucune séquence trouvée avec l\'ID: ' + seq_id)
    else:
        
        return render(request, 'genome/blast.html', {'sequences': sequences})
## Annotations
# Rôles validateur et annotateur
def a_v_role_required(user):
    if user.is_authenticated:
        return user.role in ['validateur', 'annotateur']
    return False

@user_passes_test(a_v_role_required, login_url='/login/')
def annotations(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            email = request.user.email
            annotations = Annotations.objects.filter(email_annot__email=email, annotation_status='attribué')
            if annotations:
                context = {'annotations': annotations}
                return render(request, 'genome/annotations.html', context)
            else:
                context = {'message': "Aucune séquence n'a été attribuée"}
                return render(request, 'genome/annotations.html', context)
        else:
            return redirect('login')

## Formulaire de l'annotation
@user_passes_test(a_v_role_required, login_url='/login/')
def formulaire_annotation(request, annotation_id):
    if request.method == 'GET':
        annotation = Annotations.objects.filter(annot_id=annotation_id)[0]
        if request.user.email == annotation.email_annot.email:
            context = {'annotation': annotation}
            return render(request,"genome/formulaire_annotation.html", context)
        else:
            return redirect('login')

@user_passes_test(a_v_role_required, login_url='/login/')
def formulaire_annotation(request, annotation_id):
    if request.method == 'GET':
        annotation = Annotations.objects.filter(annot_id=annotation_id)[0]
        if request.user.email == annotation.email_annot.email:
            context = {'annotation': annotation}
            return render(request,"genome/formulaire_annotation.html", context)
        else:
            return redirect('login')
    if request.method == 'POST':
        sens = request.POST.get('Brin')
        seq_biotype = request.POST.get('biotype')
        description = request.POST.get('description')
        annot = Annotations.objects.get(annot_id=annotation_id)
        annot.seq_biotype = seq_biotype
        annot.strand = sens
        annot.description = description
        annot.annotation_status = 'en cours'
        annot.save()
        message = "L'annotation pour la séquence '{}' a bien été enregistrée. Un validateur va analyser cette anotations.".format(annot.sequence_id.seq_id)
        context = {'message': message}
        return render(request,"genome/success.html", context)
