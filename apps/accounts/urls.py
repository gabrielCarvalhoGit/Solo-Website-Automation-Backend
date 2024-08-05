from django.urls import path, include

from .views import (reset_password, list_users, create_user, delete_user)


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('usuarios-cadastrados/', list_users, name='usuarios-cadastrados'),
    path('adicionar-usuario/', create_user, name='adicionar-usuario'),
    path('reset-password/', reset_password, name='reset-password'),
    path('excluir-usuario/<uuid:id>', delete_user, name='excluir-usuario'),
]