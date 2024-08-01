from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import User
from .tasks import send_email_user
from .forms import ResetPasswordForm, CreateUserForm
from .utils import generate_refresh_token, validate_jwt_token


@login_required(login_url='/accounts/login')
@permission_required('accounts.view_user', login_url='/accounts/login', raise_exception=False)
def list_users(request):
    empresa = request.user.empresa
    users = User.objects.all().filter(empresa=empresa).exclude(id=request.user.id)

    return render(request, 'accounts/list_users.html', {'users': users})

@login_required(login_url='/accounts/login')
@permission_required('accounts.add_user', login_url='/accounts/login', raise_exception=False)
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            empresa = request.user.empresa
            user = form.save(empresa=empresa)

            token = generate_refresh_token(user)
            link_redefinicao = f"{settings.SITE_URL}/accounts/reset-password/?token={token}"

            send_email_user.delay(user, link_redefinicao)
            
            # html_content = render_to_string('email/email_reset_user.html', {'user': user, 'link': link_redefinicao})
            # text_content = strip_tags(html_content)

            # email = EmailMultiAlternatives(
            #     'Solo Solutions - Mudar senha do usuário',
            #     text_content,
            #     settings.EMAIL_HOST_USER,
            #     [user.email]
            # )
            # email.attach_alternative(html_content, 'text/html')
            # email.send()

            return redirect('usuarios-cadastrados')
    
    form = CreateUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})

@login_required(login_url='/accounts/login')
@permission_required('accounts.delete_user', login_url='/accounts/login', raise_exception=False)
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()

    messages.info(request, 'Usuário excluído com sucesso')
    return redirect('usuarios-cadastrados')

def reset_password(request):
    token = request.GET.get('token')
    refresh_token = validate_jwt_token(token)

    if request.user.is_authenticated:
        return redirect('/')
    
    if not refresh_token:
        return redirect('login')
    
    user_id = refresh_token['user_id']
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['password']
            user.set_password(new_password)
            user.save()

            refresh_token.blacklist()

            messages.success(request, 'Senha redefinida com sucesso.')
            return redirect('login')
    
    form = ResetPasswordForm()
    return render(request, 'accounts/reset_password.html', {'form': form})