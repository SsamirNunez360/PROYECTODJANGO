#!/usr/bin/env python
"""
Script para probar la autenticación con la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, '/var/www/html/PROYECTODJANGO/tutoria/mysite')

django.setup()

from usuarios.models import UsuarioPersonalizado

print("=" * 70)
print("PRUEBA DE AUTENTICACIÓN")
print("=" * 70)

# Obtener usuarios
usuarios = UsuarioPersonalizado.objects.all()
print(f"\nTotal de usuarios: {usuarios.count()}\n")

# Probar autenticación
for user in usuarios[:5]:
    print(f"Usuario: {user.nombre} ({user.email})")
    print(f"  Tipo: {user.tipo}")
    print(f"  Password en BD: {user.password}")
    
    # Probar con contraseña 'admin123'
    if user.check_password('admin123'):
        print(f"  ✓ Contraseña 'admin123' es correcta")
    else:
        print(f"  ✗ Contraseña 'admin123' es incorrecta")
    
    print()

print("=" * 70)
print("PRUEBA COMPLETADA")
print("=" * 70)
