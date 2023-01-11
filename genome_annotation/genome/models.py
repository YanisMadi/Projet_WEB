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

class User(models.Model):

    ROLES = [('admin', 'Admin'),('reader', 'Reader'),('annotator', 'Annotator'),('validator', 'Validator')]

    # email de l'utilisateur
    email = models.CharField(max_length=200,null=False,primary_key=True, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    role = models.TextField(choices=ROLES,default='Reader')
    password = models.CharField(max_length=30,null=False)


class Genome(models.Model):
    accession_number = models.IntegerField(primary_key=True, blank=False)
    species = models.CharField(max_length=100)
    strain = models.CharField(max_length=100)
    seq_length = models.IntegerField(null=False)
    seq_sequence = models.TextField(null=False)


class SequenceInfo(models.Model):

    DNA_TYPE = [('chr', 'chromosome'),('plm', 'plasmide')]
    STRAND_TYPE = [('backward','-1'),('forward','+1')]
    ANNOTATED = 'yes'
    NOT_ANNOTATED = 'no'
    ANNOTATION = [('yes','annotated'),('no','not annotated')]

    sequence_id = models.CharField(max_length=20,primary_key=True, blank=False)
    email_annot = models.CharField(max_length=200)
    accesssion_number = models.IntegerField()
    dna_type = models.TextField(choices=DNA_TYPE,default='chromosome')
    start = models.PositiveIntegerField(null=False)
    end = models.PositiveBigIntegerField(null=False)
    CDS_size = models.PositiveIntegerField()
    CDS_sequence = models.TextField()
    strand = models.TextField(choices=STRAND_TYPE,default='forward')
    annotated_state = models.TextField(choices=ANNOTATION, default='no')
    pep_sequence = models.TextField()
    pep_size = models.PositiveIntegerField()

    # person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Annotations (models.Model):

    STATUS = [('validated','val'),('processing', 'proc'),('rejected', 'rej')]

    annot_id = models.IntegerField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE)
    geneID = models.CharField(max_length=100)
    sequence_id = models.ForeignKey(SequenceInfo,on_delete=models.CASCADE)
    Biotype = models.CharField(max_length=100)
    comments = models.CharField(max_length=800)
    annotation_status = models.CharField(max_length=100, choices=STATUS)
