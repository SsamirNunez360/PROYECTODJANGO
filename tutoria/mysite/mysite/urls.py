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
    path('estudiantes_perfil/', views.estudiantes_perfil, name='estudiantes_perfil'),
    path('registrar_estudiante/', views.registrar_estudiante, name='registrar_estudiante'),
    path('listar_estudiante/', views.listar_estudiante, name='listar_estudiante'),
    path('solicitud_tutoria/', views.solicitar_tutoria, name='solicitud_tutoria'),
    path('ver_solicitudes/', views.listar_solicitudes, name='ver_solicitudes'),
]
