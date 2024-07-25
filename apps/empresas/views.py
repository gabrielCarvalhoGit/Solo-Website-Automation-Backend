from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Empresa
from .tasks import enviar_email_empresa
from .forms import EmpresaCreateForm, EmpresaEditForm
from .utils import generate_refresh_token, set_automacoes_empresa
from apps.automacoes.models import Automacao
from apps.accounts.models import User


@login_required(login_url='/accounts/login')
@permission_required('empresas.view_empresa', login_url='/accounts/login', raise_exception=False)
def list_empresas(request):
    empresas = Empresa.objects.all().order_by('nome')

    return render(request, 'empresas/list_empresas.html', {'empresas': empresas})

@login_required(login_url='/accounts/login')
@permission_required('empresas.add_empresa', login_url='/accounts/login', raise_exception=False)
def create_empresa(request):
    automacoes = Automacao.objects.all()

    if request.method == 'POST':
        form = EmpresaCreateForm(request.POST)

        if form.is_valid():
            empresa = form.save(commit=False)
            email = form.cleaned_data['email']

            is_user = User.objects.filter(email=email).exists()

            if is_user:
                messages.error(request, 'O e-mail informado já está associado a um usuário existente.')
                return redirect('adicionar-empresa')
            
            empresa.save()
            set_automacoes_empresa(request, empresa)

            password_temp = User.objects.make_random_password(length=10)
            user = User.objects.create_user(
                email=email,
                password=password_temp,
                empresa_id=empresa.id
            )
            user.save()

            token = generate_refresh_token(user)

            link_redefinicao = f"{settings.SITE_URL}/accounts/reset-password/?token={token}"
            enviar_email_empresa.delay(empresa.nome, email, link_redefinicao)

            # html_content = render_to_string('email/email_empresa_cadastrada.html', {'empresa': empresa, 'link': link_redefinicao})
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
        
    form = EmpresaCreateForm()
    return render(request, 'empresas/add_empresa.html', {'form': form, 'automacoes': automacoes})

@login_required(login_url='/accounts/login')
@permission_required('empresas.change_empresa', login_url='/accounts/login', raise_exception=False)
def edit_empresa(request, id):
    empresa = get_object_or_404(Empresa, pk=id)
    automacoes = Automacao.objects.all()
    form = EmpresaEditForm(instance=empresa)

    if request.method == 'POST':
        form = EmpresaEditForm(request.POST, instance=empresa)

        if form.is_valid():
            empresa = form.save()
            set_automacoes_empresa(request, empresa)

            return redirect('empresas-cadastradas')
        else:
            return render(request, 'empresas/edit_empresa.html', {'form': form, 'empresa': empresa, 'automacoes': automacoes})
    else:
        return render(request, 'empresas/edit_empresa.html', {'form': form, 'empresa': empresa, 'automacoes': automacoes})
    
@login_required(login_url='/accounts/login')
@permission_required('empresas.delete_empresas', login_url='/accounts/login', raise_exception=False)
def delete_empresa(request, id):
    empresa = get_object_or_404(Empresa, pk=id)
    empresa.delete()

    messages.info(request, 'Empresa excluída com sucesso')
    return redirect('empresas-cadastradas')