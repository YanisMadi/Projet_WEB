from django import forms

class DatabaseForm(forms.Form):
    DATABASES = (
        ('InterPro', 'InterPro'),
        ('Ensembl', 'Ensembl'),
        ('Uniprot', 'Uniprot'),
    )
    Choisir_une_banque_de_données_externe = forms.ChoiceField(choices=DATABASES)
    id_databank = forms.CharField(label="Identifiant de la banque de données")
