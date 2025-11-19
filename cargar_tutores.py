#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para cargar tutores desde JSON a la tabla tbl_Tutores en MariaDB
"""

import json
import MySQLdb

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'passwd': '123',
    'db': 'db_Tutoria'
}

def cargar_tutores_desde_json(archivo_json):
    """Cargar tutores desde archivo JSON"""
    
    try:
        # Leer archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            tutores_data = json.load(f)
        
        # Conectar a BD
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("CARGANDO TUTORES DESDE JSON A tbl_Tutores")
        print("="*80 + "\n")
        
        tutores_cargados = 0
        
        for tutor in tutores_data:
            try:
                nombre = tutor.get('nombre', '')
                email = tutor.get('email', '')
                materias_especialidad = tutor.get('materias_especialidad', [])
                id_tutor_json = tutor.get('id_usuario', '')
                
                # Buscar o crear usuario
                cursor.execute("SELECT idUsuario FROM tbl_Usuarios WHERE correo = %s", (email,))
                user_result = cursor.fetchone()
                
                if user_result:
                    idUsuario = user_result[0]
                else:
                    # Crear usuario si no existe
                    apellido = ''
                    if ' ' in nombre:
                        partes = nombre.rsplit(' ', 1)
                        nombre = partes[0]
                        apellido = partes[1]
                    
                    password = "password123"  # Contraseña por defecto
                    cursor.execute(
                        "INSERT INTO tbl_Usuarios (correo, contrasenia, nombre, apellido, tipo, is_active, is_staff, is_superuser, last_login, date_joined) VALUES (%s, %s, %s, %s, %s, 1, 0, 0, NOW(), NOW())",
                        (email, password, nombre, apellido, 'Tutor')
                    )
                    conn.commit()
                    idUsuario = cursor.lastrowid
                
                # Insertar en tbl_Tutores
                materias_json = json.dumps(materias_especialidad) if isinstance(materias_especialidad, list) else json.dumps([materias_especialidad])
                
                cursor.execute(
                    "INSERT INTO tbl_Tutores (idUsuario, id_tutor_json, materias_especialidad) VALUES (%s, %s, %s)",
                    (idUsuario, id_tutor_json, materias_json)
                )
                conn.commit()
                
                tutores_cargados += 1
                print(f"✅ Tutor cargado: {nombre} ({email})")
                print(f"   Materias: {', '.join(materias_especialidad)}")
            
            except Exception as e:
                print(f"❌ Error al procesar tutor: {e}")
                conn.rollback()
        
        print("\n" + "="*80)
        print(f"RESUMEN DE CARGA:")
        print(f"  Tutores cargados: {tutores_cargados}")
        print("="*80 + "\n")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo_json}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # Ruta al archivo JSON de tutores
    archivo = '/var/www/html/PROYECTODJANGO/tutoria/mysite/mysite/data/tutores.json'
    cargar_tutores_desde_json(archivo)
