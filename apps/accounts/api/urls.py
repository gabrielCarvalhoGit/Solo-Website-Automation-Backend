from django.urls import path
from .views import get_routes, get_cookies_access_token, MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', get_routes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/get-cookies-token', get_cookies_access_token, name='get_cookies_token'),
]