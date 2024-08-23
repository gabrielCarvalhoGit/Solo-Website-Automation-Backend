from rest_framework import serializers
from ..models import User

class UpdateUserNameSerializer(serializers.Serializer):
    nome = serializers.CharField(required=True)

class UpdateProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        return instance