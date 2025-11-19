#!/usr/bin/env python
"""
Script de diagnóstico para verificar el estado de la base de datos y autenticación.
"""

import os
import sys
import django

sys.path.insert(0, '/var/www/html/PROYECTODJANGO/tutoria/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from usuarios.models import UsuarioPersonalizado
from django.contrib.auth import authenticate

def diagnostico():
    """Ejecuta diagnóstico de la BD."""
    
    print("="*70)
    print("DIAGNÓSTICO DEL SISTEMA DE AUTENTICACIÓN")
    print("="*70)
    
    # 1. Verificar conexión a BD
    print("\n1. Estado de la base de datos:")
    try:
        total_usuarios = UsuarioPersonalizado.objects.count()
        print(f"   ✓ Conexión a MariaDB OK")
        print(f"   ✓ Total de usuarios en BD: {total_usuarios}")
    except Exception as e:
        print(f"   ✗ Error conectando a BD: {e}")
        return
    
    # 2. Listar usuarios
    if total_usuarios > 0:
        print("\n2. Usuarios registrados en la BD:")
        for usuario in UsuarioPersonalizado.objects.all():
            print(f"   - {usuario.nombre} {usuario.apellido}")
            print(f"     Email: {usuario.email}")
            print(f"     Tipo: {usuario.tipo}")
            print(f"     ID: {usuario.idUsuario}")
    else:
        print("\n2. ⚠ No hay usuarios en la base de datos")
        print("   → Debes cargar los usuarios desde JSON primero")
    
    # 3. Probar autenticación
    print("\n3. Prueba de autenticación:")
    if total_usuarios > 0:
        usuario_test = UsuarioPersonalizado.objects.first()
        print(f"   Intentando con: {usuario_test.email}")
        
        # Intentar con contraseña correcta
        user = authenticate(username=usuario_test.email, password='12345678')
        if user is not None:
            print(f"   ✓ Autenticación exitosa con '12345678'")
        else:
            print(f"   ✗ Autenticación fallida con '12345678'")
            print(f"   → Verifica que la contraseña sea correcta")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    diagnostico()
