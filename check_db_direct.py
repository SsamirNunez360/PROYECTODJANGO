#!/usr/bin/env python
"""
Script simple para conectar a MariaDB y verificar los datos
"""
import MySQLdb

# Credenciales de conexión
HOST = 'localhost'
USER = 'admin'
PASSWORD = '123'
DATABASE = 'db_Tutoria'

try:
    # Conectar a la base de datos
    conn = MySQLdb.connect(
        host=HOST,
        user=USER,
        passwd=PASSWORD,
        db=DATABASE,
        charset='utf8mb4'
    )
    
    cursor = conn.cursor()
    print("=" * 70)
    print("VERIFICACIÓN DIRECTA DE MARIADB")
    print("=" * 70)
    
    # 1. Verificar tabla
    print("\n1. ESTRUCTURA DE TABLA tbl_Usuarios:")
    cursor.execute("DESCRIBE tbl_Usuarios")
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]}")
    
    # 2. Contar usuarios
    print("\n2. CONTEO DE USUARIOS:")
    cursor.execute("SELECT COUNT(*) FROM tbl_Usuarios")
    count = cursor.fetchone()[0]
    print(f"   Total: {count} usuarios")
    
    # 3. Listar usuarios
    print("\n3. USUARIOS EN LA BASE DE DATOS:")
    cursor.execute("SELECT idUsuario, correo, nombre, apellido, tipo, contrasenia FROM tbl_Usuarios LIMIT 10")
    for row in cursor.fetchall():
        print(f"\n   ID: {row[0]}")
        print(f"   Email: {row[1]}")
        print(f"   Nombre: {row[2]} {row[3]}")
        print(f"   Tipo: {row[4]}")
        print(f"   Contraseña (primeros 50 chars): {str(row[5])[:50]}...")
    
    print("\n" + "=" * 70)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
