from django.urls import path
from .views import MyTokenObtainPairView, refresh_access_token, get_user_session, get_routes, logout_user


urlpatterns = [
    path('', get_routes),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', refresh_access_token, name='token_refresh'),
    path('api/token/logout/', logout_user, name='logout_user'),
    path('api/token/get-user-session/', get_user_session, name='get_user_session'),
    
]