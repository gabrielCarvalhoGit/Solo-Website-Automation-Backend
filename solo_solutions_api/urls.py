from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.solo.urls')),
    path('empresas/', include("apps.empresas.urls")),
    path('accounts/', include("apps.accounts.urls")),
    path('automacoes/', include("apps.automacoes.urls")),

    path('api/accounts/', include('apps.accounts.api.urls')),
    path('api/empresas/', include('apps.empresas.api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)