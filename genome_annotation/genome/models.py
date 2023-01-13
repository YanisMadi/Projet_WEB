from django.db import models

class GenomeAnnotation(models.Model):
    # Champ de type texte de longueur maximale 100 caractères
    gene_name = models.TextField()
    # Champ de type texte de longueur maximale 500 caractères
    description = models.TextField()
    # Champ de type nombre entier
    start_position = models.IntegerField()
    # Champ de type nombre entier
    end_position = models.IntegerField()
    # Champ de type choix limité
    strand = models.CharField(max_length=1, choices=[('+', 'Forward'), ('-', 'Reverse')])

class User(models.Model):

    ROLES = [('admin', 'Admin'),('lecteur', 'Lecteur'),('annotateur', 'Annotateur'),('valideur', 'Valideur')]

    # email de l'utilisateur
    email = models.TextField(primary_key=True, blank=False)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    numero_tel = models.IntegerField()
    role = models.TextField(choices=ROLES,default='lecteur')
    motdepasse = models.TextField(null=False)


class Genome(models.Model):
    num_accession = models.IntegerField(primary_key=True, blank=False)
    espece = models.TextField()
    souche = models.TextField()
    sequence_seq = models.TextField()
    longueur_seq = models.PositiveIntegerField()


class SequenceInfo(models.Model):

    DNA_TYPE = [('chr', 'chromosome'),('plm', 'plasmide')]
    STRAND_TYPE = [('backward','-1'),('forward','+1')]
    ANNOTATION = [('oui','annoté'),('no,','non annoté')]

    sequence_id = models.TextField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE)
    num_accession = models.ForeignKey(Genome,on_delete=models.CASCADE)
    type_adn = models.TextField(choices=DNA_TYPE,default='chromosome')
    start = models.IntegerField()
    end = models.IntegerField()
    sequence_CDS = models.TextField()
    longueur_CDS = models.PositiveIntegerField()
    sequence_pep = models.TextField()
    longueur_pep = models.PositiveIntegerField()
    strand = models.TextField(choices=STRAND_TYPE,default='forward')
    annotated_state = models.TextField(choices=ANNOTATION, default='non annoté')
    

class Annotations(models.Model):

    STATUS = [('validé','val'),('en cours', 'en attente'),('rejeté', 'rej')]

    annot_id = models.IntegerField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE)
    genome_ID = models.ForeignKey(Genome,on_delete=models.CASCADE)
    sequence_id = models.ForeignKey(SequenceInfo,on_delete=models.CASCADE)
    Biotype = models.CharField(max_length=100)
    comments = models.TextField()
    annotation_status = models.TextField(choices=STATUS,default='en attente')
