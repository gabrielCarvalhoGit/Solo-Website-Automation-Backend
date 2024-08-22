from django.urls import path
from .views import MyTokenObtainPairView, refresh_access_token, logout_user, data, get_routes, update_user_name

urlpatterns = [
    path('', get_routes, name='api_root'),
    path('update-user-name/', update_user_name, name='update_user_name'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/logout/', logout_user, name='logout_user'),
    path('token/refresh/', refresh_access_token, name='token_refresh'),
    path('token/get-user-data/', get_user_session, name='get_user_data')
]
