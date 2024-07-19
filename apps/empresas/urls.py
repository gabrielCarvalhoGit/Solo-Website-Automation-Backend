from django.urls import path

from .views import (list_empresas, create_empresa)


urlpatterns = [
    path('', list_empresas, name='empresas-cadastradas'),
    path('adicionar-empresa/', create_empresa, name='adicionar-empresa'),
]