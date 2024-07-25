from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .models import Automacao


@login_required(login_url='/accounts/login')
def list_automacoes(request):
    if request.user.has_perm('automacoes.add_automacao'):
        automacoes = Automacao.objects.all().order_by('created_at')