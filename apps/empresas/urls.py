from django.urls import path

from .views import (list_empresas, create_empresa, edit_empresa, delete_empresa)


urlpatterns = [
    path('', list_empresas, name='empresas-cadastradas'),
    path('adicionar-empresa/', create_empresa, name='adicionar-empresa'),
    path('editar-empresa/<uuid:id>', edit_empresa, name='editar-empresa'),
    path('excluir-empresa/<uuid:id>', delete_empresa, name='excluir-empresa')
]