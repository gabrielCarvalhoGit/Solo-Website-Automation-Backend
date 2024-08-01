from django import forms
from django.core.exceptions import ValidationError

from .models import Empresa
from apps.accounts.models import User


class EmpresaCreateForm(forms.ModelForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('Já existe um usuário com este e-mail.')
        return email

    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco']

class EmpresaEditForm(forms.ModelForm):
    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco']