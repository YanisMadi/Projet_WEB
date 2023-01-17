from django.shortcuts import render
from .models import Annotations, User
from .forms.inscription_form import InscriptionForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages


def annotation_list(request):
    # Récupérer toutes les annotations de génome de la base de données
    annotations = Annotations.objects.all()
    # Créer un contexte de données à passer au template
    context = {'annotations': annotations}
    # Rendre le template avec le contexte de données
    return render(request, 'genome/annotation_list.html', context)

def annot_menu(request):
    return render(request, 'genome/annot_menu.html', {
        'css_files': ['home_page.css'],
    })

def login_view(request):
    return render(request, 'genome/login.html', {
        'css_files': ['login.css'],
    })

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Vérification que l'adresse email n'est pas déjà utilisée
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'Cette adresse email est déjà utilisée.')
            # Vérification que les mots de passe correspondent
            elif form.cleaned_data['motdepasse'] != form.cleaned_data['confirm_mdp']:
                form.add_error('motdepasse', 'Les mots de passe ne correspondent pas.')
                form.add_error('confirm_mdp', 'Les mots de passe ne correspondent pas.')
            else:
                # Enregistrement des données d'inscription dans la base de données
                user = form.save()
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
                return redirect('annot_menu')
    else:
        form = InscriptionForm()

    return render(request, 'genome/inscription.html', {
        'form': form,
        'css_files': ['Inscription.css'],
    })


def formulaire_genome(request) :

    return render(request, 'genome/formulaire.html', {
        'css_files': ['form.css'],
    })
