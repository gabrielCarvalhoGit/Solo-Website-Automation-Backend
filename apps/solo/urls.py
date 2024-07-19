from django.urls import path

from .views import (solo_website)


urlpatterns = [
    path('', solo_website, name='solo-website')
]