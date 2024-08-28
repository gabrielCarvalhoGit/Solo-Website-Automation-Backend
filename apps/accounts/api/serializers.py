from rest_framework import serializers
from ..models import User

class UpdateUserNameSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['nome']

    def update(self, instance, validated_data):
        nome = validated_data.get('nome')
        instance.nome = nome

        instance.save()
        return instance

class UpdateProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        profile_picture = validated_data.get('profile_picture')
        instance.profile_picture = profile_picture

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.profile_picture:
            # Retorna apenas o caminho relativo
            representation['profile_picture_url'] = instance.profile_picture.url
        else:
            representation['profile_picture_url'] = None

        return representation
    
class DeleteProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        if instance.profile_picture:
            instance.profile_picture.delete(save=False)
            instance.profile_picture = None

            instance.save()
        else:
            raise serializers.ValidationError({'detail': 'O usuário não possui foto de perfil para excluir.'})
        
        return instance