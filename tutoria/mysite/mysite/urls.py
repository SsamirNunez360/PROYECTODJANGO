from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciar', views.iniciar, name='iniciar'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('/', views.index, name='index'),
    path('tutores_perfil/', views.tutores_perfil, name='tutores_perfil'),
    path('registrar_estudiante/', views.registrar_estudiante, name='registrar_estudiante'),
    path('listar_estudiante/', views.listar_estudiante, name='listar_estudiante'),
]
