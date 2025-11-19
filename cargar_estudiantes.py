#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para cargar estudiantes desde JSON a la base de datos MariaDB
Carga datos en tbl_Estudiantes y tbl_HistorialAcademico
"""

import json
import MySQLdb
from datetime import datetime

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'passwd': '123',
    'db': 'db_Tutoria'
}

def cargar_estudiantes_desde_json(archivo_json):
    """Cargar estudiantes desde archivo JSON"""
    
    try:
        # Leer archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            estudiantes = json.load(f)
        
        # Conectar a BD
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("CARGANDO ESTUDIANTES DESDE JSON")
        print("="*80 + "\n")
        
        estudiantes_cargados = 0
        historiales_cargados = 0
        
        for estudiante in estudiantes:
            try:
                nombre = estudiante.get('nombre', '')
                email = estudiante.get('email', '')
                tipo_usuario = estudiante.get('tipo_usuario', 'Estudiante')
                nivel_academico = estudiante.get('nivel_academico', '')
                materias_interes = estudiante.get('materias_interes', [])
                historial_tutorias = estudiante.get('historial_tutorias', [])
                id_usuario_json = estudiante.get('id_usuario', '')
                
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
                        (email, password, nombre, apellido, tipo_usuario)
                    )
                    conn.commit()
                    idUsuario = cursor.lastrowid
                
                # Insertar en tbl_Estudiantes
                materias_json = json.dumps(materias_interes) if isinstance(materias_interes, list) else json.dumps([materias_interes])
                
                cursor.execute(
                    "INSERT INTO tbl_Estudiantes (idUsuario, id_usuario_json, nivel_academico, materias_interes) VALUES (%s, %s, %s, %s)",
                    (idUsuario, id_usuario_json, nivel_academico, materias_json)
                )
                conn.commit()
                idEstudiante = cursor.lastrowid
                
                estudiantes_cargados += 1
                print(f"✅ Estudiante cargado: {nombre} ({email})")
                
                # Cargar historial académico
                for sesion in historial_tutorias:
                    try:
                        idSesion = sesion.get('id_sesion', '')
                        idTutor_str = sesion.get('id_tutor', '')
                        # Convertir T001, T002, etc. a número (1, 2, etc.)
                        try:
                            idTutor = int(idTutor_str.replace('T', '')) if idTutor_str else None
                        except:
                            idTutor = None
                        materia = sesion.get('materia', '')
                        fecha_hora = sesion.get('fecha_hora', datetime.now().isoformat())
                        estado = sesion.get('estado', '')
                        calificacion = sesion.get('calificacion_dada', None)
                        
                        cursor.execute(
                            "INSERT INTO tbl_HistorialAcademico (idEstudiante, idSesion, idTutor, materia, fecha_hora, estado, calificacion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (idEstudiante, idSesion, idTutor, materia, fecha_hora, estado, calificacion)
                        )
                        conn.commit()
                        historiales_cargados += 1
                    except Exception as e:
                        print(f"   ⚠️  Error al cargar sesión: {e}")
                        conn.rollback()
                
                if historial_tutorias:
                    print(f"   └─ {len(historial_tutorias)} sesiones de tutoría cargadas")
            
            except Exception as e:
                print(f"❌ Error al procesar estudiante: {e}")
                conn.rollback()
        
        print("\n" + "="*80)
        print(f"RESUMEN DE CARGA:")
        print(f"  Estudiantes cargados: {estudiantes_cargados}")
        print(f"  Historiales cargados: {historiales_cargados}")
        print("="*80 + "\n")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo_json}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # Ruta al archivo JSON
    archivo = '/var/www/html/PROYECTODJANGO/tutoria/mysite/mysite/data/estudiantes.json'
    cargar_estudiantes_desde_json(archivo)
