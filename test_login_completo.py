#!/usr/bin/env python
"""
Script para simular el flujo completo de login
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, '/var/www/html/PROYECTODJANGO/tutoria/mysite')

django.setup()

from mysite.clases import PlataformaTutorias, ResultadoLogin
from usuarios.models import UsuarioPersonalizado

print("=" * 70)
print("PRUEBA DE LOGIN COMPLETO")
print("=" * 70)

# Crear una instancia de la plataforma
plataforma = PlataformaTutorias()

# Datos de prueba
test_cases = [
    ("admin@outlook.com", "admin123", True),
    ("ssamirnunez@outlook.com", "admin123", True),
    ("almabetancourth@outlook.com", "admin123", True),
    ("admin@outlook.com", "contraseña_incorrecta", False),
    ("usuario_inexistente@outlook.com", "admin123", False),
]

print("\nProbando casos de login:\n")

for email, password, expected_success in test_cases:
    print(f"Email: {email}")
    print(f"Contraseña: {password}")
    
    resultado = plataforma.iniciar_sesion(email, password)
    
    if resultado is not None:
        print(f"  ✓ LOGIN EXITOSO")
        print(f"    Nombre: {resultado.usuario.nombre}")
        print(f"    Email: {resultado.usuario.email}")
        print(f"    Tipo: {resultado.tipo}")
        print(f"    ID Usuario: {resultado.usuario.idUsuario}")
        
        if not expected_success:
            print(f"  ⚠ ADVERTENCIA: Se esperaba fallo pero tuvo éxito")
    else:
        print(f"  ✗ LOGIN FALLIDO")
        if expected_success:
            print(f"  ✗ ERROR: Se esperaba éxito pero falló")
    
    print()

print("=" * 70)
print("PRUEBA COMPLETADA")
print("=" * 70)
