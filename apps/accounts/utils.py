from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .models import User

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