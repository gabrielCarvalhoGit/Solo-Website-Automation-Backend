import jwt
from datetime import datetime, timedelta, timezone

from django.conf import settings
from rest_framework.exceptions import ValidationError, NotFound

from core.services.email_service import EmailService

from apps.accounts.models import User
from apps.empresas.services.empresa_service import EmpresaService
from apps.accounts.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.email_service = EmailService()

    def get_user(self, request):
        user_id = request.user.id

        try:
            user = self.repository.get_user_by_id(user_id)
            return user
        except User.DoesNotExist:
            raise NotFound('Usuário não encontrado.')

    def get_users_empresa(self, request):
        empresa_id = request.user.empresa.id if request.user.empresa else None

        if empresa_id is None:
            raise ValidationError('O usuário não está associado a nenhuma empresa cadastrada.')
        
        try:
            empresa = EmpresaService().get_empresa(empresa_id)
            users_empresa = self.repository.get_users_by_empresa(empresa.id)
            
            return users_empresa
        except NotFound:
            raise NotFound('Empresa não encontrada.')

    def create_user(self, request, **validated_data):
        empresa = request.user.empresa
        password_temp = self.repository.generate_password_temp()

        validated_data['empresa'] = empresa
        validated_data['password'] = password_temp

        if self.repository.validate_email(validated_data['email']):
            raise ValidationError('Este e-mail já está em uso.')
        
        user = self.repository.create(**validated_data)

        try:
            payload_token = {
                'user_id': str(user.id),
                'email': user.email,
                'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            }
            token = jwt.encode(payload_token, settings.SECRET_KEY, algorithm='HS256')

            self.email_service.send_reset_password_email(token, user.email)
        except Exception as e:
            raise ValidationError(str(e))
        
        return user

    def update_user(self, user, **validated_data):
        return self.repository.update(user, **validated_data)

    def process_email_change(self, user, **validated_data):
        email_atual = validated_data['email_atual']
        email_novo = validated_data['email_novo']

        if email_atual != user.email:
            raise ValidationError('O e-mail atual informado não corresponde ao e-mail cadastrado.')
        
        if self.repository.validate_email(email_novo):
            raise ValidationError('Este e-mail já está em uso.')
        
        try:
            payload = {
                'user_id': str(user.id),
                'email_atual': email_atual,
                'email_novo': email_novo,
                'exp': datetime.now(timezone.utc) + timedelta(hours=1),
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            self.email_service.send_request_email_change(token, email_novo)
        except Exception as e:
            raise ValidationError(str(e))