from django import forms
from ..models import User

class SendMessageForm(forms.Form):
    destinataire = forms.ModelChoiceField(queryset=User.objects.all())
    message = forms.CharField(widget=forms.Textarea)

class ViewMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, disabled=True)
    envoyeur = forms.CharField(disabled=True)
    timestamp = forms.CharField(disabled=True)