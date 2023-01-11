# Generated by Django 4.1.3 on 2023-01-11 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('accession_number', models.IntegerField(primary_key=True, serialize=False)),
                ('species', models.CharField(max_length=100)),
                ('strain', models.CharField(max_length=100)),
                ('seq_length', models.IntegerField()),
                ('seq_sequence', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SequenceInfo',
            fields=[
                ('sequence_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('email_annot', models.CharField(max_length=200)),
                ('accesssion_number', models.IntegerField()),
                ('dna_type', models.TextField(choices=[('chr', 'chromosome'), ('plm', 'plasmide')], default='chromosome')),
                ('start', models.PositiveIntegerField()),
                ('end', models.PositiveBigIntegerField()),
                ('CDS_size', models.PositiveIntegerField()),
                ('CDS_sequence', models.TextField()),
                ('strand', models.TextField(choices=[('backward', '-1'), ('forward', '+1')], default='forward')),
                ('annotated_state', models.TextField(choices=[('yes', 'annotated'), ('no', 'not annotated')], default='no')),
                ('pep_sequence', models.TextField()),
                ('pep_size', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField()),
                ('role', models.TextField(choices=[('admin', 'Admin'), ('reader', 'Reader'), ('annotator', 'Annotator'), ('validator', 'Validator')], default='Reader')),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Annotations',
            fields=[
                ('annot_id', models.IntegerField(primary_key=True, serialize=False)),
                ('geneID', models.CharField(max_length=100)),
                ('Biotype', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=800)),
                ('annotation_status', models.CharField(choices=[('validated', 'val'), ('processing', 'proc'), ('rejected', 'rej')], max_length=100)),
                ('email_annot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genome.user')),
                ('sequence_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genome.sequenceinfo')),
            ],
        ),
    ]
