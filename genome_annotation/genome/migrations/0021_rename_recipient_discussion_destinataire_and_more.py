# Generated by Django 4.0.4 on 2023-02-08 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0020_discussion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussion',
            old_name='recipient',
            new_name='destinataire',
        ),
        migrations.RenameField(
            model_name='discussion',
            old_name='sender',
            new_name='envoyeur',
        ),
    ]