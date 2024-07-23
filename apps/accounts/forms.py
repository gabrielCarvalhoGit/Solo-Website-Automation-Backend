from django import forms
from django.contrib.auth.password_validation import validate_password

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}),
        validators=[validate_password],
        label='Nova Senha'
    )