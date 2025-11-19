#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para cargar sesiones desde JSON a la tabla tbl_Sesiones en MariaDB
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

def cargar_sesiones_desde_json(archivo_json):
    """Cargar sesiones desde archivo JSON"""
    
    try:
        # Leer archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            sesiones_data = json.load(f)
        
        # Conectar a BD
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("CARGANDO SESIONES DESDE JSON A tbl_Sesiones")
        print("="*80 + "\n")
        
        sesiones_cargadas = 0
        
        # Iterar sobre las sesiones del JSON
        for sesion in sesiones_data:
            try:
                id_sesion_json = sesion.get('id_sesion', '')
                id_estudiante = sesion.get('id_estudiante', '')
                id_tutor = sesion.get('id_tutor', '')
                materia = sesion.get('materia', '')
                fecha_hora = sesion.get('fecha_hora', '')
                estado = sesion.get('estado', 'Pendiente')
                calificacion = sesion.get('calificacion_dada', None)
                comentarios = sesion.get('comentarios', None)
                
                # Convertir id_estudiante y id_tutor (E001 → 1, T001 → 1)
                try:
                    idEstudiante = int(id_estudiante.replace('E', '')) if id_estudiante else None
                except:
                    idEstudiante = None
                
                try:
                    idTutor = int(id_tutor.replace('T', '')) if id_tutor else None
                except:
                    idTutor = None
                
                # Insertar en la tabla
                cursor.execute(
                    """INSERT INTO tbl_Sesiones 
                    (id_sesion_json, idEstudiante, idTutor, materia, fecha_hora, estado, calificacion_dada, comentarios)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (id_sesion_json, idEstudiante, idTutor, materia, fecha_hora, estado, calificacion, comentarios)
                )
                conn.commit()
                sesiones_cargadas += 1
                print(f"✅ Sesión cargada: {id_sesion_json} - {materia} ({fecha_hora})")
                
            except Exception as e:
                print(f"⚠️  Error al cargar sesión: {e}")
                conn.rollback()
        
        print("\n" + "="*80)
        print(f"RESUMEN:")
        print(f"  Sesiones cargadas: {sesiones_cargadas}")
        print("="*80 + "\n")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo_json}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # Ruta al archivo JSON de sesiones
    archivo = '/var/www/html/PROYECTODJANGO/tutoria/mysite/mysite/data/sesiones.json'
    cargar_sesiones_desde_json(archivo)
