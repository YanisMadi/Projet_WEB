# Generated by Django 4.0.4 on 2023-02-03 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0006_user_has_module_perms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='has_module_perms',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.TextField(choices=[('lecteur', 'Lecteur'), ('annotateur', 'Annotateur'), ('validateur', 'Validateur')], default='lecteur'),
        ),
    ]