from django.urls import path, include

from .views import reset_password


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('reset-password/', reset_password, name='reset-password'),
]