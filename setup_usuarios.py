#!/usr/bin/env python
"""
Script para cargar usuarios desde JSON a la base de datos MariaDB.
Uso: python setup_usuarios.py
"""

import os
import sys
import json
import django

# Configurar Django
sys.path.insert(0, '/var/www/html/PROYECTODJANGO/tutoria/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from usuarios.models import UsuarioPersonalizado

def cargar_usuarios():
    """Carga usuarios desde archivos JSON a la base de datos."""
    
    base_path = '/var/www/html/PROYECTODJANGO/tutoria/mysite/mysite/data'
    
    # Primero, limpiar usuarios existentes
    print("Eliminando usuarios existentes...")
    UsuarioPersonalizado.objects.all().delete()
    print("✓ Base de datos limpiada.\n")
    
    archivos = {
        'estudiantes.json': 'Estudiante',
        'tutores.json': 'Tutor',
    }
    
    usuarios_creados = 0
    
    for archivo, tipo_usuario in archivos.items():
        ruta = os.path.join(base_path, archivo)
        
        if not os.path.exists(ruta):
            print(f"⚠ No se encontró: {ruta}")
            continue
        
        print(f"Cargando {archivo}...")
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                usuarios_data = json.load(f)
        except Exception as e:
            print(f"✗ Error al leer {archivo}: {e}")
            continue
        
        for usuario_dict in usuarios_data:
            try:
                email = usuario_dict.get('email')
                nombre = usuario_dict.get('nombre', 'Desconocido')
                apellido = usuario_dict.get('apellido', '')
                
                if not email:
                    print(f"  ⚠ Usuario sin email ignorado: {nombre}")
                    continue
                
                # Crear usuario con contraseña por defecto
                usuario = UsuarioPersonalizado.objects.create_user(
                    email=email,
                    password='12345678',  # Contraseña por defecto
                    nombre=nombre,
                    apellido=apellido,
                    tipo=tipo_usuario
                )
                
                usuarios_creados += 1
                print(f"  ✓ {nombre} ({email}) - {tipo_usuario}")
                
            except Exception as e:
                print(f"  ✗ Error creando usuario {usuario_dict.get('email')}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✓ {usuarios_creados} usuarios cargados exitosamente a la BD")
    print(f"{'='*60}")
    print("\nCredenciales de prueba:")
    print("  Email: anbetancourth@unah.hn")
    print("  Contraseña: 12345678")

if __name__ == '__main__':
    cargar_usuarios()
