from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Empresa
from .serializers import EmpresaSerializer, EmpresaCreateSerializer


class CustomPagePagination(PageNumberPagination):
    page_size = 7
    page_query_param = 'page'
    max_page_size = 50

@api_view(['GET'])
def empresas_list(request):
    empresas = Empresa.objects.all()
    total_empresas = Empresa.total_empresas()

    pagination_class = CustomPagePagination()
    paginated_queryset = pagination_class.paginate_queryset(empresas, request)

    serializer = EmpresaSerializer(paginated_queryset, many=True)

    return pagination_class.get_paginated_response({
        "total_empresas": total_empresas,
        "empresas": serializer.data
    })

@api_view(['POST'])
def create_empresa(request):
    serializer = EmpresaCreateSerializer(data=request.data)

    if serializer.is_valid():
        empresa = serializer.save()
        empresa_serializer = EmpresaSerializer(empresa, many=False)

        return Response({'empresa': empresa_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_empresa_by_name(request):
    nome = request.query_params.get('nome')
    if nome:
        try:
            empresa = Empresa.objects.get(nome=nome)
            empresa.delete()
            return Response({'detail': 'Empresa deletada com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        except Empresa.DoesNotExist:
            return Response({'detail': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'detail': 'Nome não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'api/empresas/': 'GET list of empresas',
        'api/empresas/list-empresas/': 'GET list of empresas with pagination',
        'api/empresas/create-empresa': 'POST create a new empresa',
        'api/empresas/delete-by-name/': 'DELETE delete an empresa'
    }

    return Response(api_urls)
