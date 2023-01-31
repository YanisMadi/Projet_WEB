from django.shortcuts import render, redirect
from .models import Annotations, User, Genome, SequenceInfo
from .forms.inscription_form import InscriptionForm
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
    # Récupérer toutes les annotations de génome de la base de données
    query_param={}
    query_param['annotation_status'] = 'en attente'
    annotations = Annotations.objects.filter(**query_param)
    # Rendre le template avec le contexte de données
    return render(request, 'genome/annotation_list.html',{'annotations': annotations})

# Page de connexion au site 
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
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
        else:
            # Message d'erreur si les identifiants sont incorrects
            messages.error(request, "Email ou mot de passe incorrect.")
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


@user_passes_test(validateur_required, login_url='/login/')
def validate_annotation(request):
    if request.method == "GET":
        annotations = Annotations.objects.filter(annotation_status='en attente')
        return render(request, 'genome/validation.html', {'annotations': annotations})
    if request.method == "POST":
        count_validated = 0
        count_rejected = 0
        for annot in Annotations.objects.filter(annotation_status='en attente'):
            if request.POST.get('validate_reject_' + str(annot.annot_id)) == 'validate':
                annot.annotation_status = 'val'
                annot.comments = request.POST.get('comment_' + str(annot.annot_id))
                annot.save()
                count_validated += 1
                send_mail(
                    'Annotation Validée',
                    'Votre annotation ID ('+str(annot.annot_id)+') a été validée avec le commentaire suivant : ' + annot.comments,
                    'cypsgenome@gmail.com',
                    [annot.email_annot],
                    fail_silently=False,
                )
            elif request.POST.get('validate_reject_' + str(annot.annot_id)) == 'reject':
                annot.annotation_status = 'rej'
                annot.comments = request.POST.get('comment_' + str(annot.annot_id))
                annot.save()
                count_rejected += 1
                send_mail(
                    'Annotation Rejetée',
                    'Votre annotation ID ('+str(annot.annot_id)+') a été rejetée avec le commentaire suivant : ' + annot.comments,
                    'cypsgenome@gmail.com',
                    [annot.email_annot],
                    fail_silently=False,
                )
        message = ""
        if count_validated > 0:
            message += str(count_validated) + " annotations ont été validées. "
        if count_rejected > 0:
            message += str(count_rejected) + " annotations ont été rejetées. "

        return HttpResponse(message)


def role_required(user):
    if user.is_authenticated:
        return user.role in ['validateur', 'annotateur', 'lecteur']
    return False

@user_passes_test(role_required, login_url='/login/')
def show_sequences(request, cds_seq, pep_seq, id_databank):
    url_ncbi = f"https://www.ncbi.nlm.nih.gov/protein/{id_databank}"
    url_ensembl = f"http://bacteria.ensembl.org/Multi/Search/Results?species=all;idx=;q={id_databank};"
    contents = urllib.request.urlopen(url_ensembl).read().decode("utf-8")
    result = re.findall(r'<a class="name" href="/(.+?)">', contents)
    url_ensembl = f"http://bacteria.ensembl.org/{result[0]}"
    contents2 = urllib.request.urlopen(url_ensembl).read().decode("utf-8")
    result2 = re.findall(r'<a href="http://www.uniprot.org/uniprot/(.+?)"', contents2)
    url_uniprot = f"http://www.uniprot.org/uniprot/{result2[0]}"

    return render(request, "sequences.html", {
        "cds_seq": cds_seq,
        "pep_seq": pep_seq,
        "url_ncbi": url_ncbi,
        "url_ensembl": url_ensembl,
        "url_uniprot": url_uniprot,
    })

@user_passes_test(role_required, login_url='/login/')
def formulaire_genome(request):
    if request.method == 'GET':
        return render(request, 'genome/formulaire.html', {
        'css_files': ['form.css'],
        })
    if request.method == 'POST':
        accessionnb = request.POST.get('accessionnb')
        espece = request.POST.get('espèce')
        souche = request.POST.get('souche')
        taille_seq = request.POST.get('taille_seq')
        idsequence = request.POST.get('idsequence')
        adn_type = request.POST.get('adn_type')
        cds_start = request.POST.get('cds_start')
        cds_end = request.POST.get('cds_end')
        Brin = request.POST.get('Brin')
        cds_seq = request.POST.get('cds_seq')
        cds_taille = request.POST.get('cds_taille')
        pep_seq = request.POST.get('pep_seq')
        pep_size = request.POST.get('pep_size')
        geneid = request.POST.get('geneid')
        gene_biotype = request.POST.get('gene_biotype')
        output_type = request.POST.get('output_type')
        if output_type == 'genome':
            query_params = {}
            if accessionnb:
                query_params['num_accession'] = accessionnb
            if espece:
                query_params['espece__icontains'] = espece
            if souche:
                query_params['souche__icontains'] = souche
            if taille_seq:
                query_params['longueur'] = taille_seq
            if adn_type:
                query_params['type_adn__icontains'] = adn_type
            genomes = Genome.objects.filter(**query_params)
            return render(request, 'genome/genome_info.html', {'genomes': genomes})
        elif output_type == 'gene_protein':
            query_params = {}
            if idsequence:
                query_params['sequence_id'] = idsequence
            if cds_start:
                query_params['start'] = cds_start
            if cds_end:
                query_params['end'] = cds_end
            if Brin:
                query_params['strand'] = Brin
            if cds_seq:
                query_params['sequence_CDS__icontains'] = cds_seq
            if cds_taille:
                query_params['longueur_CDS'] = cds_taille
            if pep_seq:
                query_params['sequence_pep__icontains'] = pep_seq
            if pep_size:
                query_params['longueur_pep'] = pep_size
            if geneid:
                query_params['gene_id'] = geneid
            if gene_biotype:
                query_params['gene_biotype__icontains'] = gene_biotype
            sequences = SequenceInfo.objects.filter(**query_params)
            return render(request, 'genome/gene_protein_info.html', {'sequences': sequences})
    


# Admin 
def admin_required(user):
    return user.is_staff

@user_passes_test(admin_required)
def manage_users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'genome/manage_users.html', context)

@user_passes_test(admin_required)
def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = User.objects.create_user(email=email, password=password, role=role)
        user.save()
        return redirect('manage_users')
    return render(request, 'genome/create_user.html')

@user_passes_test(admin_required)
def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('manage_users')

@user_passes_test(admin_required)
def assign_role(request, user_id):
    if request.method == 'POST':
        role = request.POST.get('role')
        user = User.objects.get(id=user_id)
        user.role = role
        user.save()
        return redirect('manage_users')
    return render(request, 'genome/assign_role.html', {'user': User.objects.get(id=user_id), 'roles': User.ROLES})