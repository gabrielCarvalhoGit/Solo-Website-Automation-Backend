from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Empresa
from .serializers import EmpresaSerializer, EmpresaCreateSerializer


@api_view(['GET'])
def empresas_list(request):
    empresas = Empresa.objects.all()
    total_empresas = Empresa.total_empresas()

    serializer = EmpresaSerializer(empresas, many=True)
    return Response({
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

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'api/empresas/',
        'api/empresas/list-empresas/',
        'api/empresas/empresa-detail',
        'api/empresas/create-empresa'
    }

    return Response(api_urls)