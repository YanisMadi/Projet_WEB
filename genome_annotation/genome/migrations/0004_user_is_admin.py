# Generated by Django 4.0.4 on 2023-02-03 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0003_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
