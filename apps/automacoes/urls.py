from django.urls import path

from .views import list_automacoes


urlpatterns = [
    path('', list_automacoes, name='automacoes-rpa')
]