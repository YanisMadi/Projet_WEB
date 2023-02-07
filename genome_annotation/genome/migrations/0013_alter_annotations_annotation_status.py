# Generated by Django 4.0.4 on 2023-02-04 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0012_alter_annotations_annotation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotations',
            name='annotation_status',
            field=models.TextField(choices=[('validé', 'val'), ('attribué', 'att'), ('en cours', 'en attente'), ('rejeté', 'rej')], default='attribué'),
        ),
    ]
