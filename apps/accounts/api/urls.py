from django.urls import path
from .views import MyTokenObtainPairView, refresh_access_token, logout_user, get_user_session, get_routes, update_user_name, update_profile_picture, delete_profile_picture

urlpatterns = [
    path('', get_routes, name='api_root'),
    path('update-user-name/', update_user_name, name='update_user_name'),
    path('update-profile-picture/', update_profile_picture, name='update_profile_picture'),
    path('delete-profile-picture/', delete_profile_picture, name='delete_profile_picture'),
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/logout/', logout_user, name='logout_user'),
    path('token/refresh/', refresh_access_token, name='token_refresh'),
    path('token/get-user-session/', get_user_session, name='get_user_session')
]