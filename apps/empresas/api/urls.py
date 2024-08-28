from django.urls import path
from .views import api_overview, empresas_list, create_empresa


urlpatterns = [
    path('', api_overview, name='api_overview'),
    path('list-empresas/', empresas_list, name='list_empresas'),
    path('create-empresa/', create_empresa, name='create_empresa')
]