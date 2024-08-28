import re
import uuid
from django.db import models
from django.core.exceptions import ValidationError

from apps.automacoes.models import Automacao


def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve ter 14 dígitos.')

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validar_cnpj])
    endereco = models.CharField(max_length=255)
    automacoes = models.ManyToManyField(Automacao)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.cnpj = re.sub(r'\D', '', self.cnpj)
        super().save(*args, **kwargs)
    
    @classmethod
    def total_empresas(self):
        return Empresa.objects.count()

    def __str__(self):
        return self.nome