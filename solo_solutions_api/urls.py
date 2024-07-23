from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.solo.urls')),
    path('empresas/', include("apps.empresas.urls")),
    path('accounts/', include("apps.accounts.urls")),
]