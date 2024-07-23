from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def validate_jwt_token(token):
    try:
        refresh_token = RefreshToken(token)
        
        if BlacklistedToken.objects.filter(token__jti=refresh_token['jti']).exists():
            return None
        
        return refresh_token
    except TokenError:
        return None