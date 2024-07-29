from celery import shared_task
from .models import Automacao
from django.core.files.base import ContentFile


@shared_task
def criar_automacao(nome, descricao, nome_arquivo, arquivo_temp_path):
    descricao = descricao if descricao else ''

    with open(arquivo_temp_path, 'rb') as f:
        arquivo_content = f.read()

    automacao = Automacao(nome=nome, descricao=descricao)
    automacao.arquivo.save(nome_arquivo, ContentFile(arquivo_content))

    automacao.save()

@shared_task
def editar_automacao(id, nome, descricao, arquivo):
    pass