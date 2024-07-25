import uuid
from django.db import models
from django.core.exceptions import ValidationError


def validar_formato_arquivo(arquivo):
    if not arquivo.name.endswith('.exe'):
        raise ValidationError('O arquivo informado não está no formato correto (.exe)')

class Automacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='automacoes', validators=[validar_formato_arquivo])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome