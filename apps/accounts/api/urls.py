from django.urls import path
from .views import MyTokenObtainPairView, refresh_access_token, get_cookies_access_token, get_routes, logout_user


urlpatterns = [
    path('', get_routes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', refresh_access_token, name='token_refresh'),
    path('api/token/logout/', logout_user, name='logout_user'),
    path('token/get-cookies-token', get_cookies_access_token, name='get_cookies_token'),
    
]