from django.db import models

class GenomeAnnotation(models.Model):
    # Champ de type texte de longueur maximale 100 caractères
    gene_name = models.CharField(max_length=100)
    # Champ de type texte de longueur maximale 500 caractères
    description = models.CharField(max_length=500)
    # Champ de type nombre entier
    start_position = models.IntegerField()
    # Champ de type nombre entier
    end_position = models.IntegerField()
    # Champ de type choix limité
    strand = models.CharField(max_length=1, choices=[('+', 'Forward'), ('-', 'Reverse')])

