#!/usr/bin/env python
"""
Script de diagnóstico para verificar la conexión a MariaDB y los datos de usuarios.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, '/var/www/html/PROYECTODJANGO/tutoria/mysite')

django.setup()

from django.db import connection
from usuarios.models import UsuarioPersonalizado

print("=" * 60)
print("DIAGNÓSTICO DE BASE DE DATOS")
print("=" * 60)

# 1. Verificar conexión
print("\n1. VERIFICANDO CONEXIÓN A LA BASE DE DATOS...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"   ✓ Conectado a: {db_name}")
except Exception as e:
    print(f"   ✗ Error de conexión: {e}")
    sys.exit(1)

# 2. Verificar estructura de tabla
print("\n2. VERIFICANDO ESTRUCTURA DE TABLA tbl_Usuarios...")
try:
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE tbl_Usuarios;")
        columns = cursor.fetchall()
        print("   Columnas encontradas:")
        for col in columns:
            print(f"      - {col[0]}: {col[1]}")
except Exception as e:
    print(f"   ✗ Error al obtener estructura: {e}")

# 3. Contar usuarios
print("\n3. CONTANDO USUARIOS EN LA BASE DE DATOS...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tbl_Usuarios;")
        count = cursor.fetchone()[0]
        print(f"   Total de usuarios: {count}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 4. Listar usuarios
print("\n4. LISTANDO USUARIOS EN LA BASE DE DATOS...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT idUsuario, correo, nombre, apellido, tipo FROM tbl_Usuarios LIMIT 10;")
        usuarios = cursor.fetchall()
        if usuarios:
            print("   Usuarios encontrados:")
            for user in usuarios:
                print(f"      ID: {user[0]}, Email: {user[1]}, Nombre: {user[2]} {user[3]}, Tipo: {user[4]}")
        else:
            print("   ⚠ No hay usuarios en la tabla")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 5. Probar Django ORM
print("\n5. PROBANDO DJANGO ORM...")
try:
    usuarios_orm = UsuarioPersonalizado.objects.all()
    print(f"   Usuarios encontrados por Django ORM: {usuarios_orm.count()}")
    for user in usuarios_orm[:5]:
        print(f"      - {user.nombre} ({user.email})")
except Exception as e:
    print(f"   ✗ Error con Django ORM: {e}")

# 6. Probar autenticación
print("\n6. PROBANDO AUTENTICACIÓN...")
try:
    # Obtener el primer usuario
    with connection.cursor() as cursor:
        cursor.execute("SELECT correo FROM tbl_Usuarios LIMIT 1;")
        result = cursor.fetchone()
        if result:
            email = result[0]
            print(f"   Intentando autenticar con: {email}")
            
            try:
                usuario = UsuarioPersonalizado.objects.get(email=email)
                print(f"   ✓ Usuario encontrado: {usuario.nombre}")
                print(f"   ✓ ID Usuario: {usuario.idUsuario}")
                print(f"   ✓ Tipo: {usuario.tipo}")
                
                # Intentar con contraseña de prueba
                if usuario.check_password('123'):
                    print(f"   ✓ Contraseña '123' es correcta")
                else:
                    print(f"   ✗ Contraseña '123' es incorrecta")
                    print(f"   Verificando campo 'password': {usuario.password[:20]}...")
                    
            except UsuarioPersonalizado.DoesNotExist:
                print(f"   ✗ Usuario no encontrado por Django ORM con email: {email}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
