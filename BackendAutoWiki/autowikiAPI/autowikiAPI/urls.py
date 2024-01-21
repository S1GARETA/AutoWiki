"""
URL configuration for autowikiAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from backendAPI_user.views import *

def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('backendAPI_auto.urls')), # Auto request
    path('api/v1/', include('backendAPI_forum.urls')), # Forum request
    path('api/v1/', include('backendAPI_user.urls')), # User requests

    path('auth/', include('djoser.urls')), # djoser auth
    path('auth/', include('djoser.urls.jwt')), # djoser token

    # Catch-all маршрут для React-приложения
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='catchall'),
]

handler404 = page_not_found
