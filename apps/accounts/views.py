from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import User
from .forms import ResetPasswordForm
from .utils import validate_jwt_token


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