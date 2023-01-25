from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class User(AbstractBaseUser):
    ROLES = [('admin', 'Admin'), ('lecteur', 'Lecteur'), ('annotateur', 'Annotateur'), ('validateur', 'Validateur')]
    email = models.EmailField(primary_key=True, unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    numero_tel = models.IntegerField()
    role = models.TextField(choices=ROLES,default='lecteur')
    password = models.CharField(null=False,max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
        
    @property
    def is_active(self):
        return True
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def set_is_active(self, value):
        self.is_active = value
        self.save()
    
    def set_is_staff(self, value):
        self.is_staff = value
        self.save()
    
    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.prenom

    def get_full_name(self):
        return self.prenom + ' ' + self.nom

class UserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Les utilisateurs doivent avoir un email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save()
        return user

class Genome(models.Model):
    num_accession = models.IntegerField(primary_key=True, blank=False)
    nom_gene = models.TextField()
    espece = models.TextField()
    souche = models.TextField()
    sequence_seq = models.TextField()
    longueur_seq = models.PositiveIntegerField()
    description = models.TextField()
    adn_type = models.TextField()


class SequenceInfo(models.Model):

    DNA_TYPE = [('chr', 'chromosome'),('plm', 'plasmide')]
    STRAND_TYPE = [('backward','-1'),('forward','+1')]
    ANNOTATION = [('oui','annoté'),('no,','non annoté')]

    sequence_id = models.TextField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE)
    num_accession = models.ForeignKey(Genome,on_delete=models.CASCADE)
    type_adn = models.TextField(choices=DNA_TYPE,default='chromosome')
    start = models.IntegerField()
    end =models.IntegerField()
    sequence_CDS = models.TextField()
    longueur_CDS = models.PositiveIntegerField()
    sequence_pep = models.TextField()
    longueur_pep = models.PositiveIntegerField()
    strand = models.TextField(choices=STRAND_TYPE,default='forward')
    annotated_state = models.TextField(choices=ANNOTATION, default='non annoté')
    gene_id = models.IntegerField()
    gene_biotype = models.CharField(max_length=100)
    transcript_biotype = models.CharField(max_length=100)
    gene_symbol = models.CharField(max_length=100)
    description = models.TextField()

    

class Annotations(models.Model):

    STATUS = [('validé','val'),('en cours', 'en attente'),('rejeté', 'rej')]

    annot_id = models.IntegerField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE)
    genome_ID = models.ForeignKey(Genome,on_delete=models.CASCADE)
    sequence_id = models.ForeignKey(SequenceInfo,on_delete=models.CASCADE)
    Biotype = models.CharField(max_length=100)
    comments = models.TextField()
    annotation_status = models.TextField(choices=STATUS,default='en attente')
    gene_id = models.IntegerField()
    gene_biotype = models.CharField(max_length=100)
    transcript_biotype = models.CharField(max_length=100)
    gene_symbol = models.CharField(max_length=100)
    description = models.TextField()


