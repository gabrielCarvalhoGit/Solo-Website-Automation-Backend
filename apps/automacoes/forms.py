from django import forms
from .models import Automacao


class AutomacaoForm(forms.ModelForm):
    class Meta():
        model = Automacao
        fields = ['nome', 'descricao', 'arquivo']