from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .models import User

import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

def generate_change_email_token(request):
    user_id = request.user.id
    email_atual = request.data.get('email_atual')
    email_novo = request.data.get('email_novo')

    payload = {
        'user_id': str(user_id), 
        'email_atual': email_atual,
        'email_novo': email_novo,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def generate_reset_password_token(email):
    user = User.objects.filter(email=email).first()

    if not user:
        return None
    
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def generate_refresh_token(user):
    token = RefreshToken.for_user(user)
    return str(token)

def validate_jwt_token(token):
    try:
        refresh_token = RefreshToken(token)
        
        if BlacklistedToken.objects.filter(token__jti=refresh_token['jti']).exists():
            return None
        
        return refresh_token
    except TokenError:
        return None
    
def generate_temp_password():
    return User.objects.make_random_password(length=10)