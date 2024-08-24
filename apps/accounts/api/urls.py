from django.urls import path
from .views import MyTokenObtainPairView, refresh_access_token, logout_user, request_password_reset, reset_password, get_user_session, get_routes, update_user_name, update_profile_picture, delete_profile_picture, request_email_change, confirm_email_change

urlpatterns = [
    path('', get_routes, name='api_root'),  # Rota principal para listar as rotas disponíveis
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/logout/', logout_user, name='logout_user'),
    path('token/refresh/', refresh_access_token, name='token_refresh'),
    path('reset-password/', reset_password, name='reset-password'),
    path('update-user-name/', update_user_name, name='update_user_name'),  # Rota para atualizar o nome do usuário
    path('token/get-user-session/', get_user_session, name='get_user_session'),  # Rota para obter a sessão do usuário
    path('delete-profile-picture/', delete_profile_picture, name='delete_profile_picture'),
    path('update-profile-picture/', update_profile_picture, name='update_profile_picture'),
    path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('api/confirm-email-change/', confirm_email_change, name='confirm-email-change'),
    path('api/request-email-change/', request_email_change, name='request-email-change'),
]