# Generated by Django 4.1.3 on 2023-02-07 13:05

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RenameField(
            model_name='genome',
            old_name='longueur_seq',
            new_name='longueur',
        ),
        migrations.RenameField(
            model_name='genome',
            old_name='description',
            new_name='sequence',
        ),
        migrations.RenameField(
            model_name='sequenceinfo',
            old_name='sequence_CDS',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='sequenceinfo',
            old_name='end',
            new_name='longueur',
        ),
        migrations.RenameField(
            model_name='sequenceinfo',
            old_name='sequence_pep',
            new_name='seq_cds',
        ),
        migrations.RenameField(
            model_name='sequenceinfo',
            old_name='start',
            new_name='seq_end',
        ),
        migrations.RenameField(
            model_name='sequenceinfo',
            old_name='sequence_id',
            new_name='seq_id',
        ),
        migrations.RemoveField(
            model_name='annotations',
            name='Biotype',
        ),
        migrations.RemoveField(
            model_name='genome',
            name='nom_gene',
        ),
        migrations.RemoveField(
            model_name='genome',
            name='sequence_seq',
        ),
        migrations.RemoveField(
            model_name='genome',
            name='souche',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='email_annot',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='longueur_CDS',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='longueur_pep',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirm_mdp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='motdepasse',
        ),
        migrations.AddField(
            model_name='annotations',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='annotations',
            name='seq_biotype',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='annotations',
            name='strand',
            field=models.TextField(choices=[('-1', '-1'), ('1', '1'), ('n.a.', 'n.a.')], default='n.a.'),
        ),
        migrations.AddField(
            model_name='genome',
            name='annotated_genome',
            field=models.CharField(choices=[('annoté', 'annoté'), ('non annoté,', 'non annoté')], default='non annoté', max_length=12),
        ),
        migrations.AddField(
            model_name='genome',
            name='type_adn',
            field=models.CharField(choices=[('chr', 'chromosome'), ('plm', 'plasmide')], default='chromosome', max_length=10),
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='cds',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='fonction',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='pep',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='seq_biotype',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='seq_name',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='seq_pep',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequenceinfo',
            name='seq_start',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=0, max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='annotations',
            name='annot_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='annotations',
            name='annotation_status',
            field=models.TextField(choices=[('validé', 'val'), ('attribué', 'att'), ('en cours', 'en attente'), ('rejeté', 'rej')], default='attribué'),
        ),
        migrations.AlterField(
            model_name='genome',
            name='espece',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='genome',
            name='num_accession',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sequenceinfo',
            name='annotated_state',
            field=models.CharField(choices=[('annoté', 'annoté'), ('non annoté,', 'non annoté')], default='non annoté', max_length=12),
        ),
        migrations.AlterField(
            model_name='sequenceinfo',
            name='num_accession',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='sequenceinfo',
            name='strand',
            field=models.TextField(choices=[('-1', '-1'), ('1', '1'), ('n.a.', 'n.a.')], default='n.a.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.TextField(choices=[('lecteur', 'Lecteur'), ('annotateur', 'Annotateur'), ('validateur', 'Validateur')], default='lecteur'),
        ),
    ]
