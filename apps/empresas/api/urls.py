from django.urls import path
from .views import api_overview, empresas_list, empresa_detail


urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('list-empresas/', empresas_list, name='list-empresas'),
    path('empresa-detail/<uuid:id>/', empresa_detail, name='empresa-detail'),
]