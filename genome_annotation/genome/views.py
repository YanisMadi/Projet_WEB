from django.shortcuts import render
from .models import GenomeAnnotation

def annotation_list(request):
    # Récupérer toutes les annotations de génome de la base de données
    annotations = GenomeAnnotation.objects.all()
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

def inscription(request) :

    return render(request, 'genome/inscription.html', {
        'css_files': ['inscription.css'],
    })

def formulaire_genome(request) :

    return render(request, 'genome/formulaire.html', {
        'css_files': ['form.css'],
    })