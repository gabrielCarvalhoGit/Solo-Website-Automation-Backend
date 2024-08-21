from rest_framework import serializers

class UpdateUserNameSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=100)
