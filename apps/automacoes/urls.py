from django.urls import path

from .views import list_automacoes, create_automacao, edit_automacao, delete_automacao, list_automacoes_empresa, download_automacao


urlpatterns = [
    path('', list_automacoes, name='automacoes-rpa'),
    path('adicionar-automacao', create_automacao, name='adicionar-automacao'),
    path('editar-automacao/<uuid:id>', edit_automacao, name='editar-automacao'),
    path('excluir-automacao/<uuid:id>', delete_automacao, name='excluir-automacao'),
    path('automacoes-rpa-empresa', list_automacoes_empresa, name='automacoes-rpa-empresa'),
    path('download-automacao-rpa/<uuid:id>', download_automacao, name='download-automacao-rpa')
]