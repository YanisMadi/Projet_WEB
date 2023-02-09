from django import forms
from ..models import User

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'prenom', 'nom', 'numero_tel', 'role', 'password']
