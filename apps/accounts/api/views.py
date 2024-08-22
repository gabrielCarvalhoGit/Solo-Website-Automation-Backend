from django.contrib.auth import authenticate
from ..models import User
from rest_framework import status, serializers
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.accounts.api.serializers import UpdateUserNameSerializer

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
def logout_user(request):
    try:

        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value='',
            expires=datetime.utcnow() - timedelta(days=1),
            httponly=True,
            secure=True,
            samesite='None'
        )
        response.set_cookie(
            key='access_token',
            value='',
            expires=datetime.utcnow() - timedelta(days=1),
            httponly=True,
            secure=True,
            samesite='None'
        )

        return response
    except TokenError:
        return Response({'detail': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_session(request):
    access_token = request.COOKIES.get('access_token')

    if not access_token:
        return JsonResponse({'detail': 'Autenticação necessária'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = AccessToken(access_token)
        user_id = token['user_id']
        user = User.objects.get(id=user_id)
        return JsonResponse({'Email': user.email, 'Nome': user.nome})
    except TokenError:
        return JsonResponse({'detail': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return JsonResponse({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_user_name(request):
    access_token = request.COOKIES.get('access_token')
    
    if not access_token:
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = AccessToken(access_token)
        user_id = token['user_id']
        user = User.objects.get(id=user_id)
        
        serializer = UpdateUserNameSerializer(data=request.data)
        if serializer.is_valid():
            user.nome = serializer.validated_data['nome']
            user.save()
            return Response({'detail': 'Nome atualizado com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except TokenError:
        return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/accounts/token',
        '/api/accounts/token/logout',
        '/api/accounts/token/refresh',
        '/api/accounts/token/get-user-session',
        '/api/accounts/update-user-name',  # Nova rota para atualização do nome do usuário
    ]
    return Response(routes)