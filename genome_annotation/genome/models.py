from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class User(AbstractBaseUser):
    ROLES = [('admin', 'Admin'), ('lecteur', 'Lecteur'), ('annotateur', 'Annotateur'), ('validateur', 'Validateur')]
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(primary_key=True, unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    numero_tel = models.IntegerField()
    role = models.TextField(choices=ROLES,default='lecteur')
    password = models.CharField(null=False,max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
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


    @property
    def is_validateur(self):
        return self.role == 'validateur'

    @property
    def is_annotateur(self):
        return self.role == 'annotateur'

    @property
    def is_lecteur(self):
        return self.role == 'lecteur'

    
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

class UserManager(BaseUserManager):

    def create_user(self, username, email, numero_tel, password=None, **extra_fields):
        if not email:
            raise ValueError("Les utilisateurs doivent avoir un email")
        user = self.model(username=username, email=self.normalize_email(email), numero_tel=numero_tel, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, numero_tel, password=None, **extra_fields):
        user = self.create_user(email, numero_tel, password, **extra_fields)
        user.is_admin = True
        user.save()
        return user


class Genome(models.Model):
    DNA_TYPE = [('chr', 'chromosome'),('plm', 'plasmide')]

    num_accession = models.CharField(primary_key=True, blank=False,max_length=50)
    espece = models.CharField(max_length=50)
    type_adn = models.CharField(choices=DNA_TYPE,default='chromosome',max_length=10)
    sequence = models.TextField()
    longueur = models.PositiveIntegerField()
  

class SequenceInfo(models.Model):

    DNA_TYPE = [('chr', 'Chromosome dna'),('plm', 'Plasmide dna')]
    STRAND_TYPE = [('backward','-1'),('forward','1')]
    
    num_accession = models.CharField(max_length=30) # genome_id
    type_adn = models.TextField(choices=DNA_TYPE,default=None)
    seq_id = models.TextField(primary_key=True, blank=False)
    seq_name = models.CharField(max_length=30)
    cds = models.BooleanField(default=False)
    pep = models.BooleanField(default=False)
    seq_biotype = models.CharField(max_length=30)
    fonction = models.CharField(max_length=100)
    seq_start = models.IntegerField()
    seq_end =models.IntegerField()
    seq_cds = models.TextField()
    seq_pep = models.TextField()
    longueur = models.IntegerField()
    strand = models.TextField(choices=STRAND_TYPE,default='forward')
    description = models.TextField()


class Annotations(models.Model):

    STATUS = [('validé','val'),('attribué','att'),('en cours', 'en attente'),('rejeté', 'rej')]

    annot_id = models.IntegerField(primary_key=True, blank=False)
    email_annot = models.ForeignKey(User,on_delete=models.CASCADE)
    genome_ID = models.ForeignKey(Genome,on_delete=models.CASCADE)
    sequence_id = models.ForeignKey(SequenceInfo,on_delete=models.CASCADE)
    Biotype = models.CharField(max_length=100)
    comments = models.TextField()
    annotation_status = models.TextField(choices=STATUS,default='n.a.')
    gene_id = models.IntegerField()
    gene_biotype = models.CharField(max_length=100)
    transcript_biotype = models.CharField(max_length=100)
    gene_symbol = models.CharField(max_length=100)
    description = models.TextField()

