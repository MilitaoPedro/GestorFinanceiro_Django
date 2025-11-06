"""
URL configuration for gestor_financeiro project.

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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


# Seu urls.py principal
from django.contrib import admin
from django.urls import path, include
from core.views import DashboardView # Importa a view que criamos

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rota raiz (página inicial)
    path('', DashboardView.as_view(), name='dashboard'), 
    # Inclui as rotas do app core (a ser criado a seguir)
    path('', include('core.urls')), 
    # *Se você usa um app de autenticação (ex: allauth):*
    # path('accounts/', include('allauth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]