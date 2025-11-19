#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para cargar solicitudes desde JSON a la tabla tbl_Solicitudes en MariaDB
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

def cargar_solicitudes_desde_json(archivo_json):
    """Cargar solicitudes desde archivo JSON"""
    
    try:
        # Leer archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            solicitudes_data = json.load(f)
        
        # Conectar a BD
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("CARGANDO SOLICITUDES DESDE JSON A tbl_Solicitudes")
        print("="*80 + "\n")
        
        solicitudes_cargadas = 0
        
        for solicitud in solicitudes_data:
            try:
                id_estudiante = solicitud.get('id_estudiante', '')
                materia = solicitud.get('materia', '')
                fecha_hora_preferida = solicitud.get('fecha_hora_preferida', '')
                
                # Convertir id_estudiante (E001 → 1)
                try:
                    idEstudiante = int(id_estudiante.replace('E', '')) if id_estudiante else None
                except:
                    idEstudiante = None
                
                if not idEstudiante:
                    print(f"⚠️  Estudiante inválido: {id_estudiante}")
                    continue
                
                # Verificar que el estudiante existe en tbl_Estudiantes
                cursor.execute("SELECT idEstudiante FROM tbl_Estudiantes WHERE idEstudiante = %s", (idEstudiante,))
                if not cursor.fetchone():
                    print(f"⚠️  Estudiante no existe en BD: {id_estudiante} (ID: {idEstudiante})")
                    continue
                
                # Generar ID único para la solicitud
                id_solicitud_json = f"SOL_{id_estudiante}_{materia.replace(' ', '_')}"
                
                # Insertar en la tabla
                cursor.execute(
                    """INSERT INTO tbl_Solicitudes 
                    (id_solicitud_json, idEstudiante, materia, fecha_hora_preferida, estado, fecha_creacion)
                    VALUES (%s, %s, %s, %s, %s, NOW())""",
                    (id_solicitud_json, idEstudiante, materia, fecha_hora_preferida, 'Pendiente')
                )
                conn.commit()
                solicitudes_cargadas += 1
                print(f"✅ Solicitud cargada: {id_estudiante} - {materia} - {fecha_hora_preferida}")
                
            except Exception as e:
                print(f"⚠️  Error al cargar solicitud: {e}")
                conn.rollback()
        
        print("\n" + "="*80)
        print(f"RESUMEN:")
        print(f"  Solicitudes cargadas: {solicitudes_cargadas}")
        print("="*80 + "\n")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo_json}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # Ruta al archivo JSON de solicitudes
    archivo = '/var/www/html/PROYECTODJANGO/tutoria/mysite/mysite/data/solicitudes.json'
    cargar_solicitudes_desde_json(archivo)
