from rest_framework_simplejwt.tokens import RefreshToken


def generate_refresh_token(user):
    token = RefreshToken.for_user(user)
    return str(token)