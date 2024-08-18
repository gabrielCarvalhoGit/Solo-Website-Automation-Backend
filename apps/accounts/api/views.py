from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Email ou senha inválido.")
        
        return super().validate(attrs)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response({'Erro': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = serializer.validated_data.get('refresh')
        access = serializer.validated_data.get('access')

        response = Response({
            'access': access,
            'refresh': refresh
        })

        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response

@api_view(['GET'])
def get_cookies_access_token(request):
    access_token = request.COOKIES.get('access_token')

    if not access_token:
        return Response({'Detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = AccessToken(access_token)
        user = token['user_id']
    except TokenError:
        return Response({'Detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({'Acess_token': access_token}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/token/get-cookies-token'
    ]

    return Response(routes)