from django.contrib import admin
from django.urls import path
from . import views
from mysite.lib.userlib import LibUser


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
    
    # Nueva URL para el historial de sesiones
    path('historial_sesiones/', views.historial_sesiones, name='historial_sesiones'),
    
    # URL para asignar tutorías automáticamente (si aún no la tienes)
    path('asignar_tutoria/', views.asignar_tutoria, name='asignar_tutoria'),
    
    path('solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('asignar-tutoria-manual/', views.asignar_tutoria_manual, name='asignar_tutoria_manual'),
    path('asignar_tutorias_automaticamente/', views.asignar_tutorias_automaticamente, name='asignar_tutorias_automaticamente'),
    
    path('editar_estudiante/<str:id_estudiante>/', views.editar_estudiante, name='editar_estudiante'),
    path('eliminar_estudiante/<str:id_estudiante>/', views.eliminar_estudiante, name='eliminar_estudiante'),

    path('editar_tutor/<str:id_tutor>/', views.editar_tutor, name='editar_tutor'),
    path('eliminar_tutor/<str:id_tutor>/', views.eliminar_tutor, name='eliminar_tutor'),
    
    path('completar_sesion/', views.completar_sesion, name='completar_sesion'),

]
