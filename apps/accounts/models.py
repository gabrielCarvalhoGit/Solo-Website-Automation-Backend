import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.empresas.models import Empresa


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de email deve ser fornecido')
        
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True) # Relacionamento com a tabela empresas
    nome = models.CharField(max_length=100, default='admin')
    email = models.EmailField(unique=True) # importante
    is_active = models.BooleanField(default=True) # padrão do django
    is_staff = models.BooleanField(default=False) # padrão do django
    is_admin_empresa = models.BooleanField(default=False) # verificar
    date_joined = models.DateTimeField(auto_now_add=True) # padrão do django

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('can_create_solo_admin_user', 'Can create user solo admin')
        ]

    def clean(self):
        super().clean()

    def __str__(self):
        return self.email