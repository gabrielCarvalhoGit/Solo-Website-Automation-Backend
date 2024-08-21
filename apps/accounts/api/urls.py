from django.urls import path
from .views import MyTokenObtainPairView, refresh_access_token, logout_user, get_user_session, get_routes


urlpatterns = [
    path('', get_routes),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', refresh_access_token, name='token_refresh'),
    path('token/logout/', logout_user, name='logout_user'),
    path('token/get-user-session/', get_user_session, name='get_user')
]