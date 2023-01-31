from django import forms

class DatabaseForm(forms.Form):
    DATABASES = (
        ('NCBI', 'NCBI'),
        ('Ensembl', 'Ensembl'),
        ('Uniprot', 'Uniprot'),
    )
    database = forms.ChoiceField(choices=DATABASES)
