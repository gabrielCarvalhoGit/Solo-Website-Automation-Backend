from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class TokenRefreshMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verificar se há tokens nos cookies
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        # Se o access_token está presente, verificar sua validade
        if access_token:
            if not self.is_token_valid(access_token):
                # Se o access_token for inválido, tentar usar o refresh_token para gerar um novo access_token
                if refresh_token:
                    try:
                        refresh = RefreshToken(refresh_token)
                        new_access_token = str(refresh.access_token)
                        
                        # Criar uma nova resposta para incluir o novo access_token
                        response = self.get_response(request)
                        response.set_cookie(
                            key='access_token',
                            value=new_access_token,
                            httponly=True,
                            secure=True,
                            samesite='None'
                        )
                        return response
                    except TokenError:
                        # Caso o refresh_token também seja inválido, retornar erro de sessão expirada
                        return JsonResponse({'detail': 'Sessão expirada.'}, status=401)
                else:
                    # Se não há refresh_token, retornar erro de autenticação
                    return JsonResponse({'detail': 'Autenticação necessária'}, status=401)
        
        # Se não houver access_token, simplesmente passar para o próximo middleware ou view
        return self.get_response(request)
    
    def is_token_valid(self, token):
        try:
            AccessToken(token)
            return True
        except TokenError:
            return False
