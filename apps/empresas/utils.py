from apps.accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def generate_temp_password():
    return User.objects.make_random_password(length=10)

def generate_refresh_token(user):
    token = RefreshToken.for_user(user)
    return str(token)

def set_automacoes_empresa(request, empresa):
    if 'automacoes' in request.POST:
        automacao_ids = request.POST.getlist('automacoes')
        empresa.automacoes.set(automacao_ids)