from django import forms
from .models import Empresa


class EmpresaForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco']