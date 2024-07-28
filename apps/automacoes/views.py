import mimetypes
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Automacao
from .forms import AutomacaoForm
from .tasks import criar_automacao, editar_automacao


@login_required(login_url='/accounts/login')
@permission_required('automacoes.view_automacao', login_url='/accounts/login', raise_exception=False)
def list_automacoes(request):
    automacoes = Automacao.objects.all().order_by('created_at')

    return render(request, 'automacoes/list_automacoes.html', {'automacoes': automacoes})

@login_required(login_url='/accounts/login')
@permission_required('automacoes.add_automacao', login_url='/accounts/login', raise_exception=False)
def create_automacao(request):
    if request.method == 'POST':
        form = AutomacaoForm(request.POST, request.FILES)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            arquivo = form.cleaned_data['arquivo']

            criar_automacao.delay(nome, descricao, arquivo.path)
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
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            arquivo = form.cleaned_data['arquivo']

            editar_automacao.delay(id=automacao.id, nome=nome, descricao=descricao, arquivo=arquivo.path)
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

@login_required(login_url='/accounts/login')
def list_automacoes_empresa(request):
    automacoes = request.user.empresa.automacoes.all()

    return render(request, 'automacoes/list_automacoes.html', {'automacoes': automacoes})

@login_required(login_url='/accounts/login')
def download_automacao(request, id):
    automacao = get_object_or_404(Automacao, pk=id)
    path_automacao = automacao.arquivo.path
    nome_arquivo_download = automacao.nome.replace(' ', '_') + '.exe'

    try:
        with open(path_automacao, 'rb') as f:
            mime_type, _ = mimetypes.guess_type(path_automacao)
            response = HttpResponse(f, content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename={nome_arquivo_download}'
            return response
    except FileNotFoundError:
        raise Http404("Arquivo não encontrado")