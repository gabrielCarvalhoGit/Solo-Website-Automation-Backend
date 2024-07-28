from celery import shared_task
from .models import Automacao


@shared_task
def criar_automacao(nome, descricao, arquivo):
    automacao = Automacao(nome=nome, descricao=descricao, arquivo=arquivo)
    automacao.save()

@shared_task
def editar_automacao(id, nome, descricao, arquivo):
    automacao = Automacao.objects.get(id=id)

    automacao.nome = nome
    automacao.descricao = descricao
    automacao.arquivo = arquivo

    automacao.save()