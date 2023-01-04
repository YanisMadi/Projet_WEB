from django.shortcuts import render
from .models import GenomeAnnotation

def annotation_list(request):
    # Récupérer toutes les annotations de génome de la base de données
    annotations = GenomeAnnotation.objects.all()
    # Créer un contexte de données à passer au template
    context = {'annotations': annotations}
    # Rendre le template avec le contexte de données
    return render(request, 'templates/annotation_list.html', context)
