from django.db import models

class User(models.Model):

    ROLES = [('admin', 'Admin'),('lecteur', 'Lecteur'),('annotateur', 'Annotateur'),('valideur', 'Valideur')]

    # email de l'utilisateur
    email = models.CharField(primary_key=True, blank=False, max_length=100)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    numero_tel = models.IntegerField()
    role = models.CharField(choices=ROLES,default='lecteur',max_length=10)
    motdepasse = models.CharField(null=False,max_length=50)
    confirm_mdp = models.CharField(null=False,max_length=50)


class Genome(models.Model):
    num_accession = models.IntegerField(primary_key=True, blank=False)
    nom_gene = models.CharField(max_length=50)
    espece = models.CharField(max_length=50)
    souche = models.CharField(max_length=50)
    sequence = models.TextField()
    longueur = models.PositiveIntegerField()
    description = models.CharField(max_length=1000)


class SequenceInfo(models.Model):

    DNA_TYPE = [('chr', 'chromosome'),('plm', 'plasmide')]
    STRAND_TYPE = [('backward','-1'),('forward','+1')]
    ANNOTATION = [('oui','annoté'),('no,','non annoté')]

    num_accession = models.ForeignKey(Genome,on_delete=models.CASCADE)
    type_adn = models.CharField(choices=DNA_TYPE,default='chromosome',max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(choices=STRAND_TYPE,default='forward',max_length=8)
    annotated_state = models.CharField(choices=ANNOTATION, default='non annoté',max_length=10)
    

class Annotations(models.Model):

    STATUS = [('validé','val'),('en cours', 'en attente'),('rejeté', 'rej')]

    annot_id = models.IntegerField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE,max_length=100)
    genome_ID = models.ForeignKey(Genome,on_delete=models.CASCADE,max_length=50)
    Biotype = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000)
    annotation_status = models.CharField(choices=STATUS,default='en attente',max_length=10)
