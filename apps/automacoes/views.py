from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Automacao
from .forms import AutomacaoForm


@login_required(login_url='/accounts/login')
@permission_required('automacoes.view_automacao', login_url='/accounts/login', raise_exception=False)
def list_automacoes(request):
    automacoes = Automacao.objects.all().order_by('created_at')

    return render(request, 'automacoes/list_automacoes.html', {'automacoes': automacoes})

@login_required(login_url='/accounts/login')
def list_automacoes_empresa(request):
    automacoes = request.user.empresa.automacoes.all()

    return render(request, 'automacoes/list_automacoes.html', {'automacoes': automacoes})

@login_required(login_url='/accounts/login')
@permission_required('automacoes.add_automacao', login_url='/accounts/login', raise_exception=False)
def create_automacao(request):
    if request.method == 'POST':
        form = AutomacaoForm(request.POST, request.FILES)

        if form.is_valid():
            automacao = form.save(commit=False)
            automacao.save()

            return redirect('automacoes-rpa')
    
    form = AutomacaoForm()
    return render(request, 'automacoes/add_automacao.html', {'form': form})

@login_required(login_url='/accounts/login')
@permission_required('automacoes.change_automacao', login_url='/accounts/login', raise_exception=False)
def edit_automacao(request, id):
    automacao = get_object_or_404(Automacao, pk=id)
    form = AutomacaoForm(instance=automacao)

    if request.method == 'POST':
        form = AutomacaoForm(request.POST, instance=automacao)

        if form.is_valid():
            form.save()
            return redirect('automacoes-rpa')
        else:
            return render(request, 'automacoes/edit_automacao.html', {'form': form, 'automacao': automacao})
    else:
        return render(request, 'automacoes/edit_automacao.html', {'form': form, 'automacao': automacao})
    
@login_required(login_url='/accounts/login')
@permission_required('automacoes.delete_automacao', login_url='/accounts/login', raise_exception=False)
def delete_automacao(request, id):
    automacao = get_object_or_404(Automacao, pk=id)
    automacao.delete()

    messages.info(request, 'Automação excluída com sucesso')
    return redirect('automacoes-rpa')