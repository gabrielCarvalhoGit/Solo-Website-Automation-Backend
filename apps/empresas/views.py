from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required

from .models import Empresa
from .forms import EmpresaForm
from apps.accounts.models import User


@login_required
def list_empresas(request):
    empresas = Empresa.objects.all().order_by('nome')

    return render(request, 'empresas/list_empresas.html', {'empresas': empresas})

@login_required
def create_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)

        if form.is_valid():
            empresa = form.save(commit=False)
            email = form.cleaned_data['email']

            is_user = User.objects.filter(email=email).exists()

            if is_user:
                messages.error(request, 'O e-mail informado já está associado a um usuário existente.')
                return redirect('adicionar-empresa')
            
            empresa.save()

            password_temp = User.objects.make_random_password(length=10)
            user = User.objects.create_user(
                email=email,
                password=password_temp,
                empresa_id=empresa.id
            )
            user.save()

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # html_content = render_to_string('email/email_empresa_cadastrada.html', {'empresa': empresa})
            # text_content = strip_tags(html_content)

            # email = EmailMultiAlternatives(
            #     'Solo Solutions - Mudar senha do usuário',
            #     text_content,
            #     settings.EMAIL_HOST_USER,
            #     [email]
            # )
            # email.attach_alternative(html_content, 'text/html')
            # email.send()

            return redirect('empresas-cadastradas')
        
    form = EmpresaForm()
    return render(request, 'empresas/add_empresa.html', {'form': form})