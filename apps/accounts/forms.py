from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User
from .utils import generate_temp_password


class CreateUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Já existe um usuário com este e-mail.')
        return email

    def save(self, commit=True, empresa=None):
        user = super().save(commit=False)
        password_temp = generate_temp_password()
        user.set_password(password_temp)
        user.empresa = empresa

        if commit:
            user.save()
        return user

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}),
        validators=[validate_password],
        label='Nova Senha'
    )