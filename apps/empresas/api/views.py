from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Empresa
from .serializers import EmpresaSerializer


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'api/empresas/',
        'api/empresas/list-empresas/',
        'api/empresas/empresa-detail',
    }

    return Response(api_urls)

@api_view(['GET'])
def empresas_list(request):
    empresas = Empresa.objects.all()
    serializer = EmpresaSerializer(empresas, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def empresa_detail(request, id):
    empresa = Empresa.objects.get(id=id)
    serializer = EmpresaSerializer(empresa, many=False)

    return Response(serializer.data)