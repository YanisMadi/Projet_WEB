# Generated by Django 4.0.4 on 2023-02-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0017_remove_sequenceinfo_cds_remove_sequenceinfo_pep_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequenceinfo',
            name='seq_name',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
