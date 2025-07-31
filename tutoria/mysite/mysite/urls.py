"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciar', views.iniciar, name='iniciar'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    
    
    path('dulce/', views.dulce, name='dulce'),
    path('recomendacion/', views.recomendacion, name='recomendacion'),

    path('dulce/crear/', views.create_dulce, name='create_dulce'),
    path('dulce/insert', views.insert_dulce, name='insert_dulce'),

    path('dulce/edit', views.edit_dulce, name='edit_dulce'),
    path('dulce/update', views.update_dulce, name='insert_dulce'),

    path('dulce/remove/', views.remove_dulce, name='create_dulce'),
    path('dulce/delete', views.delete_dulce, name='insert_dulce'),

    path('resenia/', views.resenia, name='resenia'),

    path('resenia/crear/', views.create_resenia, name='create_resenia'),
    path('resenia/insert', views.insert_resenia, name='insert_resenia'),

    path('resenia/edit', views.edit_resenia, name='edit_resenia'),
    path('resenia/update', views.update_resenia, name='insert_resenia'),

    path('resenia/remove/', views.remove_resenia, name='create_resenia'),
    path('resenia/delete', views.delete_resenia, name='insert_resenia'),

    path('favorito/', views.favorito, name='favorito'),

    path('favorito/crear/', views.create_favorito, name='create_favorito'),
    path('favorito/insert', views.insert_favorito, name='insert_favorito'),

    path('favorito/edit', views.edit_favorito, name='edit_favorito'),
    path('favorito/update', views.update_favorito, name='insert_favorito'),

    path('favorito/remove/', views.remove_favorito, name='create_favorito'),
    path('favorito/delete', views.delete_favorito, name='insert_favorito'),

    path('registro/', views.registro, name='registro'),

    path('registro/crear/', views.create_registro, name='create_registro'),
    path('registro/insert', views.insert_registro, name='insert_registro'),

    path('registro/edit', views.edit_registro, name='edit_registro'),
    path('registro/update/', views.update_registro, name='insert_registro'),

    path('registro/remove/', views.remove_registro, name='create_registro'),
    path('registro/delete', views.delete_registro, name='insert_registro'),

    # URLs para proveedores
    path('proveedor/', views.proveedor, name='proveedor'),
    path('proveedor/crear/', views.create_proveedor, name='create_proveedor'),
    path('proveedor/insert/', views.insert_proveedor, name='insert_proveedor'),
    path('proveedor/edit/<str:id>/', views.edit_proveedor, name='edit_proveedor'),
    path('proveedor/update/', views.update_proveedor, name='insert_proveedor'),
    path('proveedor/remove/<str:id>/', views.remove_proveedor, name='remove_proveedor'),
    path('proveedor/delete/<str:id>/', views.delete_proveedor, name='delete_proveedor'),

    path('promocion/', views.promocion, name='promocion'),
    path('promocion/crear/', views.create_promocion, name='create_promocion'),
    path('promocion/insert/', views.insert_promocion, name='insert_promocion'),
    path('promocion/edit/', views.edit_promocion, name='promocion_edit'),
    path('promocion/update/', views.update_promocion, name='insert_proveedor'),
    path('promocion/remove/<int:pk>/', views.remove_promocion, name='create_promocion'),
    path('promocion/delete/<int:pk>/', views.delete_promocion, name='insert_promocion'),

    path('buscar_dulce', views.buscar_dulce, name='buscar_dulce'),

    path('buscar_por_nombre', views.buscar_dulce, name='buscar_por_nombre'),
    path('buscar_por_marca', views.buscar_dulce, name='buscar_por_marca'),

    path('dulce/comprar', views.comprar_dulce, name='comprar_dulce'),

    path('lista_deseo/', views.lista_deseo, name='lista_deseo'),
    #path('deseos/guardar', views.guardar_en_lista_deseos, name='guardar_en_lista_deseos'),
]
