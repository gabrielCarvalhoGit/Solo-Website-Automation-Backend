from django.urls import path

from .views import list_automacoes, list_automacoes_empresa, create_automacao, edit_automacao, delete_automacao


urlpatterns = [
    path('', list_automacoes, name='automacoes-rpa'),
    path('adicionar-automacao', create_automacao, name='adicionar-automacao'),
    path('editar-automacao/<uuid:id>', edit_automacao, name='editar-automacao'),
    path('excluir-automacao/<uuid:id>', delete_automacao, name='excluir-automacao'),
    path('automacoes-rpa-empresa', list_automacoes_empresa, name='automacoes-rpa-empresa'),
]