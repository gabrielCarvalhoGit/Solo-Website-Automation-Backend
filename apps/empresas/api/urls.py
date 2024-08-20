from django.urls import path
from .views import api_overview, empresas_list, empresa_detail, create_empresa


urlpatterns = [
    path('', api_overview, name='api_overview'),
    path('list-empresas/', empresas_list, name='list_empresas'),
    path('empresa-detail/<uuid:id>/', empresa_detail, name='empresa_detail'),
    path('create-empresa/', create_empresa, name='create_empresa')
]