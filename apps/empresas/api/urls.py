from django.urls import path
from .views import get_routes, empresas_list, create_empresa, update_empresa, delete_empresa_by_name


urlpatterns = [
    path('', get_routes, name='api_overview'),
    path('list-empresas/', empresas_list, name='list_empresas'),
    path('create-empresa/', create_empresa, name='create_empresa'),
    path('update-empresa/<uuid:id>', update_empresa, name='update-empresa'),
    path('delete-by-name/', delete_empresa_by_name, name='delete_empresa_by_name'),
]