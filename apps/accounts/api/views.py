from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..models import User
from .serializers import UpdateUserNameSerializer, UpdateProfilePictureSerializer, DeleteProfilePictureSerializer
from django.contrib.auth.hashers import check_password, make_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nome'] = user.nome
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
            secure=True,
            samesite='None'
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='None'
        )

        return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({'detail': 'Refresh token não encontrado'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refresh_token)
        access = refresh.access_token
        response = Response({'access_token': str(access)}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=True,
            samesite='None'
        )
        return response
    except TokenError:
        return Response({'detail': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value='',
            expires=datetime.now(timezone.utc) - timedelta(days=1),
            httponly=True,
            secure=True,
            samesite='None'
        )

        response.set_cookie(
            key='refresh_token',
            value='',
            expires=datetime.now(timezone.utc) - timedelta(days=1),
            httponly=True,
            secure=True,
            samesite='None'
        )

        return response
    except TokenError:
        return Response({'detail': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_name(request):
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        serializer = UpdateUserNameSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({'detail': 'Nome atualizado com sucesso'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_picture(request):
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        serializer = UpdateProfilePictureSerializer(user, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            response_data = serializer.to_representation(user)
            return Response({
                'detail': 'Imagem de perfil atualizada com sucesso.',
                'profile_picture_url': response_data['profile_picture_url']
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def delete_profile_picture(request):
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        serializer = DeleteProfilePictureSerializer(user, data={'profile_picture': None}, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({'detail': 'Imagem de perfil removida com sucesso'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_session(request):
    user = request.user

    try:
        profile_picture_url = user.profile_picture.url if user.profile_picture else None
        
        return Response({
            'email': user.email,
            'nome': user.nome,
            'profile_picture': profile_picture_url
        })
    except User.DoesNotExist:
        return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_email_change(request):
    user_id = request.user.id  
    email_atual = request.data.get('email_atual')
    email_novo = request.data.get('email_novo')

    payload = {
        'user_id': str(user_id), 
        'email_atual': email_atual,
        'email_novo': email_novo,
        'exp': datetime.utcnow() + timedelta(hours=1),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    url_confirmacao = f'http://localhost:3000/confirm-email/?token={token}'
    send_mail(
        'Confirme sua mudança de e-mail',
        f'Clique no link para confirmar a mudança de e-mail: {url_confirmacao}',
        'no-reply@myapp.com',
        [email_novo],
        fail_silently=False,
    )

    return Response({'message': 'E-mail de confirmação enviado com sucesso.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])  
def confirm_email_change(request):
    token = request.data.get('token')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        email_novo = payload.get('email_novo')
    except jwt.ExpiredSignatureError:
        return Response({'error': 'O token expirou.'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.InvalidTokenError:
        return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
        user.email = email_novo
        user.save()

        return Response({'message': 'E-mail atualizado com sucesso.', 'email_novo': email_novo}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()

    if not user:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    reset_link = f"http://localhost:3000/reset-password?token={token}"
    send_mail(
        'Redefinição de Senha',
        f'Clique no link para redefinir sua senha: {reset_link}',
        'noreply@solosolutions.com.br',
        [user.email],
        fail_silently=False,
    )

    return Response({"message": "Reset link sent"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request):
    token = request.data.get('token')
    senha_atual = request.data.get('senha_atual')
    senha_nova = request.data.get('senha_nova')

    if not all([token, senha_atual, senha_nova]):
        return Response({"error": "Todos os campos devem ser preenchidos corretamente."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = User.objects.get(id=user_id)

        if not check_password(senha_atual, user.password):
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(senha_nova)
        user.save()

        return Response({"message": "Senha atualizada com sucesso!"}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token expirado!"}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.InvalidTokenError:
        return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "O usuário não existe"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_routes(request):
    routes = [
        '/api/accounts/token/',
        '/api/accounts/token/logout/',
        '/api/accounts/token/refresh/',
        '/api/accounts/update-user-name/',
        '/api/accounts/update-profile-picture/',
        '/api/accounts/delete-profile-picture/',
        '/api/accounts/token/get-user-session',
        '/api/accounts/update-user-name/',
        '/api/accounts/request-password-reset/',
        '/api/accounts/reset-password/',
    ]

    return Response(routes)