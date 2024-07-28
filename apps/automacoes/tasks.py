from celery import shared_task
from .models import Automacao


@shared_task
def criar_automacao(nome, descricao, arquivo):
    descricao = descricao if descricao else ''

    with open(arquivo, 'rb') as f:
        automacao = Automacao(nome=nome, descricao=descricao)
        automacao.arquivo.save(f.name, f)

        automacao.save()

@shared_task
def editar_automacao(id, nome, descricao, arquivo):
    automacao = Automacao.objects.get(id=id)

    automacao.nome = nome
    automacao.descricao = descricao if descricao else ''

    with open(arquivo, 'rb') as f:
        automacao.arquivo.save(f.name, f)

    automacao.save()