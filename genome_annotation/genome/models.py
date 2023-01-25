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
    DNA_TYPE = [('chr', 'chromosome'),('plm', 'plasmide')]

    num_accession = models.IntegerField(primary_key=True, blank=False)
    #nom_gene = models.CharField(max_length=50)
    espece = models.CharField(max_length=50)
    #souche = models.CharField(max_length=50)
    type_adn = models.CharField(choices=DNA_TYPE,default='chromosome',max_length=10)
    sequence = models.TextField()
    longueur = models.PositiveIntegerField()
    #description = models.CharField(max_length=1000)


class SequenceInfo(models.Model):

    
    #STRAND_TYPE = [('backward','-1'),('forward','+1')]
    ANNOTATION = [('oui','annoté'),('no,','non annoté')]

    num_accession = models.CharField(max_length=30) # genome_id
    type_adn = models.CharField(max_length=30)
    seq_id = models.CharField(max_length=30, primary_key=True)
    seq_name = models.CharField(max_length=30)
    seq_type = models.CharField(max_length=30)
    seq_biotype = models.CharField(max_length=30)
    fonction = models.CharField(max_length=100)
    seq_start = models.IntegerField()
    seq_end = models.IntegerField()
    sequence = models.TextField()
    longueur = models.IntegerField()
    annotated_state = models.CharField(choices=ANNOTATION, default='non annoté',max_length=10)
    

class Annotations(models.Model):
    
    STATUS = [('validé','val'),('en cours', 'en attente'),('rejeté', 'rej')]

    annot_id = models.IntegerField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE,max_length=100)
    num_accession = models.ForeignKey(Genome,on_delete=models.CASCADE,max_length=50)
    seq_biotype = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    strand = models.CharField(choices=STRAND_TYPE,default='forward',max_length=8)
    annotation_status = models.CharField(choices=STATUS,default='en attente',max_length=10)
