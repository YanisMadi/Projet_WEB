from django.shortcuts import render, redirect
from .models import Annotations, User
from .forms.inscription_form import InscriptionForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import user_passes_test

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

# Page de tous les génomes annotés
def annotation_list(request):
    # Récupérer toutes les annotations de génome de la base de données
    annotations = Annotations.objects.all()
    # Créer un contexte de données à passer au template
    context = {'annotations': annotations}
    # Rendre le template avec le contexte de données
    return render(request, 'genome/annotation_list.html', context)

# Page de recherche de génomes annotés
def formulaire_genome(request) :
    return render(request, 'genome/formulaire.html', {
        'css_files': ['form.css'],
    })

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

# Page d'accueil des Annotateurs
def annotateur_required(user):
    return user.role == "annotateur"

@user_passes_test(annotateur_required, login_url='/login/')

def annotateur_page(request):
    return render(request, 'genome/annotateur_page.html', {
        'css_files': ['form.css'],
    })