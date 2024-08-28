from rest_framework import serializers
from ..models import Empresa
from ..utils import set_automacoes

from apps.accounts.models import User
from apps.automacoes.models import Automacao


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class EmpresaCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    automacoes = serializers.PrimaryKeyRelatedField(queryset=Automacao.objects.all(), many=True, required=False)

    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco', 'automacoes', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('O email informado ja possui um usuário cadastrado.')
        
        return value
    
    def create(self, validated_data):
        email = validated_data.pop('email')

        automacao_ids = validated_data.pop('automacoes', None)
        empresa = Empresa.objects.create(**validated_data)

        set_automacoes(automacao_ids, empresa)

        password_temp = User.objects.make_random_password()
        user = User.objects.create_user(
            email=email,
            nome='Admin',
            password=password_temp,
            is_admin_empresa=True
        )
        user.empresa = empresa
        user.save()

        return empresa