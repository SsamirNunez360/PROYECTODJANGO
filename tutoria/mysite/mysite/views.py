import os
import json
import re
import unicodedata
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.timezone import now
from pathlib import Path
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_POST




from .clases import (
    SesionTutoria,
    Usuario,
    Estudiante,
    Tutor,
    Cola,
    ArbolBinarioBusqueda,
    PlataformaTutorias,
)


def index(request):
    #resp = lista.obtener()
    return render(request,"index.html")
    #return HttpResponse("Hola mundo")
    #return render(request,"index.html",{"lista":lista.obtener()})

def login(request):
    return render(request,"login.html")


def iniciar(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        plataforma = PlataformaTutorias()
        resultado = plataforma.iniciar_sesion(email, password)

        # Si no coincide o no existe
        if resultado is None:
            messages.error(request, "Credenciales incorrectas")
            return render(request, "login.html")

        # Guardar datos del usuario en sesión
        request.session["user_email"] = resultado.usuario.email
        request.session["user_id"] = str(resultado.usuario.idUsuario)
        request.session["user_type"] = resultado.tipo
        request.session["user_name"] = resultado.usuario.nombre

        # Redirigir a home (página principal después del login)
        messages.success(request, f"¡Bienvenido {resultado.usuario.nombre}!")
        return redirect("home")

    # GET → mostrar login
    return render(request, "login.html")



def registrar_estudiante(request):
    import MySQLdb
    import json
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        nivel = request.POST.get('nivel_academico')
        materias = request.POST.getlist('materias_interes')
        
        try:
            conn = MySQLdb.connect(host='localhost', user='admin', passwd='123', db='db_Tutoria')
            cursor = conn.cursor()
            
            # Crear usuario en tbl_Usuarios
            from usuarios.models import UsuarioPersonalizado
            usuario = UsuarioPersonalizado.objects.create_user(
                email=email,
                password='123456',  # Contraseña por defecto
                tipo='Estudiante'
            )
            
            # Insertar en tbl_Estudiantes
            materias_json = json.dumps(materias, ensure_ascii=False)
            cursor.execute(
                """INSERT INTO tbl_Estudiantes (idUsuario, nivel_academico, materias_interes)
                VALUES (%s, %s, %s)""",
                (usuario.idUsuario, nivel, materias_json)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            from django.contrib import messages
            messages.success(request, f"Estudiante {nombre} registrado correctamente.")
            return redirect('estudiantes_perfil')
            
        except Exception as e:
            print(f"Error al registrar estudiante: {e}")
            from django.contrib import messages
            messages.error(request, f"Error al registrar: {str(e)}")
            return render(request, 'registrar_estudiante.html')

    return render(request, 'registrar_estudiante.html')


def editar_estudiante(request, id_estudiante):
    import MySQLdb
    import json
    from django.contrib import messages
    
    try:
        idEstudiante = int(id_estudiante.replace('E', '')) if id_estudiante else None
    except:
        idEstudiante = None
    
    try:
        conn = MySQLdb.connect(host='localhost', user='admin', passwd='123', db='db_Tutoria')
        cursor = conn.cursor()
        
        # Obtener estudiante y sus datos
        cursor.execute(
            """SELECT e.idEstudiante, e.idUsuario, e.nivel_academico, e.materias_interes, u.correo
            FROM tbl_Estudiantes e
            JOIN tbl_Usuarios u ON e.idUsuario = u.idUsuario
            WHERE e.idEstudiante = %s""",
            (idEstudiante,)
        )
        
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            messages.error(request, "Estudiante no encontrado.")
            return redirect('estudiantes_perfil')
        
        idEstudianteDB, idUsuario, nivel_actual, materias_json, email_actual = row
        
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            nivel = request.POST.get('nivel_academico')
            materias = request.POST.getlist('materias_interes')
            
            # Actualizar usuario en tbl_Usuarios
            cursor.execute(
                """UPDATE tbl_Usuarios SET correo = %s WHERE idUsuario = %s""",
                (email, idUsuario)
            )
            
            # Actualizar estudiante en tbl_Estudiantes
            materias_json_new = json.dumps(materias, ensure_ascii=False)
            cursor.execute(
                """UPDATE tbl_Estudiantes SET nivel_academico = %s, materias_interes = %s
                WHERE idEstudiante = %s""",
                (nivel, materias_json_new, idEstudianteDB)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            messages.success(request, "Estudiante actualizado correctamente.")
            return redirect('estudiantes_perfil')
        
        # Parsear materias JSON para mostrar en formulario
        try:
            materias_lista = json.loads(materias_json) if materias_json else []
        except:
            materias_lista = []
        
        estudiante = {
            'id_usuario': f"E{idEstudianteDB:03d}",
            'nombre': 'N/A',  # El nombre está en tbl_Usuarios
            'email': email_actual,
            'nivel_academico': nivel_actual,
            'materias_interes': materias_lista
        }
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al editar estudiante: {e}")
        messages.error(request, f"Error: {str(e)}")
        return redirect('estudiantes_perfil')

    return render(request, 'editar_estudiante.html', {'estudiante': estudiante})


def eliminar_estudiante(request, id_estudiante):
    import MySQLdb
    from django.contrib import messages
    
    try:
        idEstudiante = int(id_estudiante.replace('E', '')) if id_estudiante else None
    except:
        idEstudiante = None
    
    try:
        conn = MySQLdb.connect(host='localhost', user='admin', passwd='123', db='db_Tutoria')
        cursor = conn.cursor()
        
        # Obtener idUsuario antes de eliminar
        cursor.execute("SELECT idUsuario FROM tbl_Estudiantes WHERE idEstudiante = %s", (idEstudiante,))
        row = cursor.fetchone()
        
        if not row:
            cursor.close()
            conn.close()
            messages.error(request, "Estudiante no encontrado.")
            return redirect('estudiantes_perfil')
        
        idUsuario = row[0]
        
        # Eliminar estudiante (CASCADE elimina historial automáticamente)
        cursor.execute("DELETE FROM tbl_Estudiantes WHERE idEstudiante = %s", (idEstudiante,))
        
        # Opcionalmente eliminar usuario también
        cursor.execute("DELETE FROM tbl_Usuarios WHERE idUsuario = %s", (idUsuario,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        messages.success(request, "Estudiante eliminado correctamente.")
        
    except Exception as e:
        print(f"Error al eliminar estudiante: {e}")
        messages.error(request, f"Error al eliminar: {str(e)}")
    
    return redirect('estudiantes_perfil')




def solicitar_tutoria(request):
    if request.method == 'POST':
        import MySQLdb
        
        # Obtener datos del formulario
        id_estudiante = request.POST.get('id_estudiante')
        materia = request.POST.get('materia')
        fecha_hora_raw = request.POST.get('fecha_hora_preferida')
        
        # Convertir el estudiante de E001 a 1
        try:
            idEstudiante = int(id_estudiante.replace('E', '')) if id_estudiante else None
        except:
            idEstudiante = None
        
        # Obtener y formatear la fecha
        try:
            fecha_hora_obj = datetime.strptime(fecha_hora_raw, "%Y-%m-%dT%H:%M")
            fecha_hora_str = fecha_hora_obj.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            fecha_hora_str = fecha_hora_raw.replace("T", " ")
        
        # Guardar en la BD
        try:
            conn = MySQLdb.connect(host='localhost', user='admin', passwd='123', db='db_Tutoria')
            cursor = conn.cursor()
            
            # Verificar que el estudiante existe
            cursor.execute("SELECT idEstudiante FROM tbl_Estudiantes WHERE idEstudiante = %s", (idEstudiante,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return render(request, 'solicitud_tutoria.html', {'error': 'Estudiante no encontrado'})
            
            # Generar ID único para la solicitud
            id_solicitud_json = f"SOL_{id_estudiante}_{materia.replace(' ', '_')}"
            
            # Insertar solicitud en BD
            cursor.execute(
                """INSERT INTO tbl_Solicitudes 
                (id_solicitud_json, idEstudiante, materia, fecha_hora_preferida, estado, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, NOW())""",
                (id_solicitud_json, idEstudiante, materia, fecha_hora_str, 'Pendiente')
            )
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error al guardar solicitud: {e}")
            return render(request, 'solicitud_tutoria.html', {'error': str(e)})

        return redirect('home')

    return render(request, 'solicitud_tutoria.html')



def listar_solicitudes(request):
    import MySQLdb
    
    try:
        conn = MySQLdb.connect(host='localhost', user='admin', passwd='123', db='db_Tutoria')
        cursor = conn.cursor()
        
        # Obtener solicitudes de la BD con información del estudiante
        cursor.execute(
            """SELECT s.idSolicitud, s.id_solicitud_json, s.idEstudiante, 
                      CONCAT('E', LPAD(s.idEstudiante, 3, '0')) as id_estudiante,
                      s.materia, s.fecha_hora_preferida, s.estado, s.fecha_creacion
               FROM tbl_Solicitudes s
               ORDER BY s.fecha_creacion DESC"""
        )
        
        rows = cursor.fetchall()
        solicitudes = []
        
        for row in rows:
            solicitudes.append({
                'idSolicitud': row[0],
                'id_solicitud_json': row[1],
                'idEstudiante': row[2],
                'id_estudiante': row[3],
                'materia': row[4],
                'fecha_hora_preferida': row[5],
                'estado': row[6],
                'fecha_creacion': row[7]
            })
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al obtener solicitudes: {e}")
        solicitudes = []

    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes})

# En tu archivo views.py


def asignar_tutoria_manual(request):
    """
    Procesa una solicitud específica, busca un tutor compatible
    y crea una nueva sesión de tutoría.
    """
    if request.method == 'POST':
        plataforma = PlataformaTutorias()

        # Obtener los datos de la solicitud desde el formulario
        id_estudiante = request.POST.get('id_estudiante')
        materia_solicitada = request.POST.get('materia')
        fecha_hora_preferida = request.POST.get('fecha_hora_preferida')
        
        # Normalizar la materia para una búsqueda insensible a mayúsculas y tildes
        materia_normalizada = normalize(materia_solicitada)
        
        # --- AÑADE ESTAS LÍNEAS DE DEPURACIÓN AQUÍ ---
        print("\n--- DEPURACIÓN DE ASIGNACIÓN ---")
        print(f"Solicitud: {id_estudiante}, Materia: '{materia_solicitada}', Fecha/Hora: '{fecha_hora_preferida}'")
        print(f"Materia normalizada para búsqueda: '{materia_normalizada}'")

        mejor_tutor = None
        tutores_posibles = []

        # Itera sobre cada tutor para verificar los criterios
        for tutor in plataforma.diccionario_tutores.values():
            
            # --- AGREGAMOS IMPRESIONES PARA CADA TUTOR ---
            materias_del_tutor_normalizadas = [normalize(m) for m in tutor.materias_especialidad]
            disponibilidad_tutor = tutor.disponibilidad.get(fecha_hora_preferida)

            print(f"\nRevisando tutor: {tutor.nombre}")
            print(f"Materias del tutor: {materias_del_tutor_normalizadas}")
            print(f"Disponibilidad para '{fecha_hora_preferida}': '{disponibilidad_tutor}'")
            
            # Condición para ver si el tutor es un posible candidato
            if materia_normalizada in materias_del_tutor_normalizadas and disponibilidad_tutor == 'libre':
                print(f"Tutor {tutor.nombre} CUMPLE con los criterios.")
                tutores_posibles.append(tutor)
            else:
                print(f"Tutor {tutor.nombre} NO CUMPLE con los criterios.")
        
        print("\n------------------------------")
        print(f"Tutores posibles encontrados: {tutores_posibles}")
        # --- FIN DE LAS LÍNEAS DE DEPURACIÓN ---
        
        # 2. Si se encuentra un tutor, se asigna (simplificamos tomando el primero)
        if tutores_posibles:
            mejor_tutor = tutores_posibles[0]
            
            # 3. Crear una nueva sesión de tutoría
            id_sesion = plataforma.generar_id_sesion()
            nueva_sesion = SesionTutoria(
                id_sesion=id_sesion,
                id_estudiante=id_estudiante,
                id_tutor=mejor_tutor.id_usuario,
                materia=materia_solicitada,
                fecha_hora=fecha_hora_preferida,
                estado="Confirmada"
            )

            # 4. Actualizar las estructuras de datos de la plataforma
            plataforma.historial_general_sesiones.append(nueva_sesion)
            estudiante = plataforma.diccionario_estudiantes.get(id_estudiante)
            estudiante.agregar_a_historial(nueva_sesion)
            mejor_tutor.actualizar_disponibilidad(fecha_hora_preferida, 'ocupado')
            
            # 5. Eliminar la solicitud de la cola (y del archivo JSON)
            solicitudes_pendientes = plataforma.cola_solicitudes.to_list()
            solicitudes_actualizadas = [
                s for s in solicitudes_pendientes 
                if not (s['id_estudiante'] == id_estudiante and
                        s['materia'] == materia_solicitada and
                        s['fecha_hora_preferida'] == fecha_hora_preferida)
            ]
            plataforma.cola_solicitudes.items = solicitudes_actualizadas

            # 6. Guardar todos los cambios en los archivos JSON
            plataforma._guardar_datos()
            messages.success(request, f"Tutoría asignada con éxito al tutor {mejor_tutor.nombre}.")
        else:
            messages.error(request, "No se pudo encontrar un tutor disponible para esta solicitud.")

        return redirect('listar_solicitudes')

    return redirect('listar_solicitudes')


def asignar_tutorias_automaticamente(request):
    plataforma = PlataformaTutorias()
    
    # 1. Construir el grafo de asignación
    for solicitud in plataforma.cola_solicitudes.to_list():
        materia_normalizada = normalize(solicitud['materia'])
        fecha_hora_preferida = solicitud['fecha_hora_preferida']
        
        # Nodo de la solicitud
        nodo_solicitud = f"solicitud_{solicitud['id_estudiante']}_{materia_normalizada}_{fecha_hora_preferida}"
        plataforma.grafo_asignacion.agregar_nodo(nodo_solicitud)
        
        # Nodos de horario
        nodo_horario = f"horario_{fecha_hora_preferida}"
        plataforma.grafo_asignacion.agregar_nodo(nodo_horario)
        plataforma.grafo_asignacion.agregar_arista(nodo_solicitud, nodo_horario)

        # Buscar tutores que enseñen la materia y estén libres
        for tutor in plataforma.diccionario_tutores.values():
            materias_tutor_normalizadas = [normalize(m) for m in tutor.materias_especialidad]
            
            if materia_normalizada in materias_tutor_normalizadas and tutor.disponibilidad.get(fecha_hora_preferida) == 'libre':
                # Nodo del tutor
                nodo_tutor = f"tutor_{tutor.id_usuario}"
                plataforma.grafo_asignacion.agregar_arista(nodo_horario, nodo_tutor)
                
    mensajes_exito = 0
    mensajes_error = 0
    solicitudes_a_eliminar = []

    # 2. Iterar sobre las solicitudes para encontrar la asignación óptima
    for solicitud in plataforma.cola_solicitudes.to_list():
        materia_normalizada = normalize(solicitud['materia'])
        fecha_hora_preferida = solicitud['fecha_hora_preferida']
        
        nodo_solicitud = f"solicitud_{solicitud['id_estudiante']}_{materia_normalizada}_{fecha_hora_preferida}"
        
        # Buscar tutores compatibles usando el grafo
        tutor_encontrado = None
        for tutor in plataforma.diccionario_tutores.values():
            materias_tutor_normalizadas = [normalize(m) for m in tutor.materias_especialidad]
            
            if materia_normalizada in materias_tutor_normalizadas and tutor.disponibilidad.get(fecha_hora_preferida) == 'libre':
                ruta, distancia = plataforma.grafo_asignacion.encontrar_camino_optimo(nodo_solicitud, f"tutor_{tutor.id_usuario}")
                if ruta:
                    tutor_encontrado = tutor
                    break # Se encontró un tutor, se asigna y se pasa a la siguiente solicitud

        if tutor_encontrado:
            # Asignar la tutoría
            id_sesion = plataforma.generar_id_sesion()
            nueva_sesion = SesionTutoria(
                id_sesion=id_sesion,
                id_estudiante=solicitud['id_estudiante'],
                id_tutor=tutor_encontrado.id_usuario,
                materia=solicitud['materia'],
                fecha_hora=fecha_hora_preferida,
                estado="Confirmada"
            )
            plataforma.historial_general_sesiones.append(nueva_sesion)
            estudiante = plataforma.diccionario_estudiantes.get(solicitud['id_estudiante'])
            estudiante.agregar_a_historial(nueva_sesion)
            tutor_encontrado.actualizar_disponibilidad(fecha_hora_preferida, 'ocupado')
            solicitudes_a_eliminar.append(solicitud)
            mensajes_exito += 1
        else:
            mensajes_error += 1
            
    # Eliminar las solicitudes que ya fueron asignadas
    solicitudes_pendientes = [s for s in plataforma.cola_solicitudes.to_list() if s not in solicitudes_a_eliminar]
    plataforma.cola_solicitudes.items = solicitudes_pendientes

    # Guardar los cambios
    plataforma._guardar_datos()

    if mensajes_exito > 0:
        messages.success(request, f"{mensajes_exito} tutorías asignadas automáticamente con éxito.")
    if mensajes_error > 0:
        messages.error(request, f"No se pudo encontrar tutor para {mensajes_error} solicitudes.")

    return redirect('listar_solicitudes')



def home(request):
    return render(request,"home.html")


def normalize(text):
    # Convierte a minúsculas y elimina tildes
    text = text.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def tutores_perfil(request):
    # Mostrar tutores desde la tabla tbl_Tutores en la BD
    subject = request.GET.get('subject', '').strip()
    normalized_subject = normalize(subject)

    from django.db import connection

    tutores = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.idTutor, t.id_tutor_json, u.nombre, u.apellido, u.correo, u.tipo, t.materias_especialidad
            FROM tbl_Tutores t
            JOIN tbl_Usuarios u ON t.idUsuario = u.idUsuario
            ORDER BY t.idTutor
        """)
        rows = cursor.fetchall()

    for row in rows:
        idTutor, id_tutor_json, nombre, apellido, correo, tipo_usuario, materias_raw = row
        # materias_especialidad puede ser JSON texto o una cadena; normalizar a lista
        materias_list = []
        try:
            if materias_raw:
                materias_list = json.loads(materias_raw)
                # Si viene como una sola cadena con comas, convertir a lista
                if isinstance(materias_list, str):
                    materias_list = [m.strip() for m in materias_list.split(',') if m.strip()]
        except Exception:
            # Fallback: intentar separar por comas
            if materias_raw and isinstance(materias_raw, str):
                materias_list = [m.strip() for m in materias_raw.split(',') if m.strip()]

        tutor_obj = {
            'id_usuario': id_tutor_json if id_tutor_json else f"T{idTutor:03d}",
            'nombre': f"{nombre} {apellido}".strip(),
            'email': correo,
            'tipo_usuario': tipo_usuario,
            'materias_especialidad': materias_list,
        }

        tutores.append(tutor_obj)

    # Filtrar por materia si se proporcionó
    if normalized_subject:
        tutores_filtrados = []
        for tutor in tutores:
            materias_norm = [normalize(m) for m in tutor.get('materias_especialidad', [])]
            if normalized_subject in materias_norm:
                tutores_filtrados.append(tutor)
    else:
        tutores_filtrados = tutores

    return render(request, 'tutores_perfil.html', {'tutores': tutores_filtrados, 'subject': subject})

def estudiantes_perfil(request):
    # Mostrar estudiantes desde la tabla tbl_Estudiantes en la BD
    subject = request.GET.get('subject', '').strip()
    normalized_subject = normalize(subject)

    from django.db import connection

    estudiantes = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.idEstudiante, e.id_usuario_json, u.nombre, u.apellido, u.correo, u.tipo, e.nivel_academico, e.materias_interes
            FROM tbl_Estudiantes e
            JOIN tbl_Usuarios u ON e.idUsuario = u.idUsuario
            ORDER BY e.idEstudiante
        """)
        rows = cursor.fetchall()

    for row in rows:
        idEst, id_usuario_json, nombre, apellido, correo, tipo_usuario, nivel_academico, materias_raw = row
        # materias_interes puede ser JSON texto o una cadena; normalizar a lista
        materias_list = []
        try:
            if materias_raw:
                materias_list = json.loads(materias_raw)
                # Si viene como una sola cadena con comas, convertir a lista
                if isinstance(materias_list, str):
                    materias_list = [m.strip() for m in materias_list.split(',') if m.strip()]
        except Exception:
            # Fallback: intentar separar por comas
            if materias_raw and isinstance(materias_raw, str):
                materias_list = [m.strip() for m in materias_raw.split(',') if m.strip()]

        estudiante_obj = {
            'id_usuario': id_usuario_json if id_usuario_json else f"E{idEst:03d}",
            'nombre': f"{nombre} {apellido}".strip(),
            'email': correo,
            'tipo_usuario': tipo_usuario,
            'nivel_academico': nivel_academico,
            'materias_interes': materias_list,
        }

        estudiantes.append(estudiante_obj)

    # Filtrar por materia si se proporcionó
    if normalized_subject:
        estudiantes_filtrados = []
        for estudiante in estudiantes:
            materias_norm = [normalize(m) for m in estudiante.get('materias_interes', [])]
            if normalized_subject in materias_norm:
                estudiantes_filtrados.append(estudiante)
    else:
        estudiantes_filtrados = estudiantes

    return render(request, 'estudiantes_perfil.html', {
        'estudiantes': estudiantes_filtrados,
        'subject': subject
    })



  


def registrar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        
        plataforma = PlataformaTutorias()
        if plataforma.registrar_usuario_basico(email, password, nombre, apellido):
            messages.success(request, 'Registro exitoso')
            return redirect('login')
        else:
            messages.error(request, 'El email ya está registrado')
    
    return render(request, 'registro.html')
    

def menu_principal(request):
    return render(request, 'menu.html')



def registrar_estudiante_get(request):
    return render(request, 'registrar_estudiante.html')

def listar_estudiante(request):
    return render(request, 'listar_estudiante.html')

def registrar_tutor(request):
    """
    Vista que maneja el registro de un nuevo tutor.
    """
    if request.method == 'POST':
        # Extraer los datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        materias_especialidad_str = request.POST.get('materias_especialidad')
        
        # Procesar las materias de especialidad (separar por coma)
        materias_especialidad = [m.strip() for m in materias_especialidad_str.split(',')]
        
        plataforma = PlataformaTutorias() 
        if plataforma.registrar_tutor(nombre, email, materias_especialidad):
             messages.success(request, '¡Tutor registrado exitosamente!')
             return redirect(reverse('home')) # Redirige a la página principal
        else:
            messages.error(request, 'Error al registrar el tutor. El correo electrónico ya existe.')
            return render(request, 'registrar_tutor.html')

    # Si la solicitud es GET, simplemente muestra el formulario
    return render(request, 'registrar_tutor.html')


def editar_tutor(request, id_tutor):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'tutores.json')

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            tutores = json.load(f)
    except FileNotFoundError:
        messages.error(request, "No se encontró el archivo de tutores.")
        return redirect('tutores_perfil')

    tutor = next((t for t in tutores if t['id_usuario'] == id_tutor), None)
    if not tutor:
        messages.error(request, "Tutor no encontrado.")
        return redirect('tutores_perfil')

    if request.method == 'POST':
        tutor['nombre'] = request.POST.get('nombre')
        tutor['email'] = request.POST.get('email')
        materias_str = request.POST.get('materias_especialidad')
        materias_list = request.POST.getlist('materias')
        tutor['materias_especialidad'] = [m.strip() for m in materias_list if m.strip()]


        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(tutores, f, indent=4, ensure_ascii=False)

        messages.success(request, "Tutor actualizado correctamente.")
        return redirect('tutores_perfil')

    return render(request, 'editar_tutor.html', {'tutor': tutor})


def eliminar_tutor(request, id_tutor):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'tutores.json')

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            tutores = json.load(f)
    except FileNotFoundError:
        tutores = []

    nuevos_tutores = [t for t in tutores if t['id_usuario'] != id_tutor]

    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(nuevos_tutores, f, indent=4, ensure_ascii=False)

    messages.success(request, "Tutor eliminado correctamente.")
    return redirect('tutores_perfil')



def ver_perfil(request):
    return render(request, 'ver_perfil.html')

def listar_estudiantes(request):
    return render(request, 'listar_estudiantes.html')

def listar_tutores(request):
    return render(request, 'listar_tutores.html')

def actualizar_usuario(request):
    return render(request, 'actualizar_usuario.html')

def eliminar_usuario(request):
    return render(request, 'eliminar_usuario.html')

'''
def solicitar_tutoria(request):
    return render(request, 'solicitud_tutoria.html')

def listar_solicitudes(request):
    return render(request, 'listar_solicitudes.html')
'''

def asignar_tutoria(request):
    return render(request, 'asignar_tutoria.html')

def completar_sesion(request):
    return render(request, 'completar_sesion.html')





def historial_sesiones(request):
    # Leer sesiones desde la tabla tbl_Sesiones en la BD
    from django.db import connection
    
    # Obtener parámetros de filtrado
    materia_filtro = request.GET.get('materia', '').strip().lower()
    estudiante_filtro = request.GET.get('estudiante', '').strip().lower()
    tutor_filtro = request.GET.get('tutor', '').strip().lower()

    try:
        sesiones = []
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.idSesion, s.id_sesion_json, s.idEstudiante, s.idTutor, s.materia, s.fecha_hora, s.estado, s.calificacion_dada, s.comentarios,
                       e.idEstudiante as est_id
                FROM tbl_Sesiones s
                LEFT JOIN tbl_Estudiantes e ON s.idEstudiante = e.idEstudiante
                ORDER BY s.fecha_hora DESC
            """)
            rows = cursor.fetchall()

        sesiones_procesadas = []
        for row in rows:
            idSesion, id_sesion_json, idEstudiante, idTutor, materia, fecha_hora, estado, calificacion_dada, comentarios, est_id = row
            
            # Construir objeto sesión compatible con template
            sesion = {
                'idSesion': idSesion,
                'id_sesion': id_sesion_json,
                'id_estudiante': f"E{idEstudiante:03d}" if idEstudiante else '',
                'id_tutor': f"T{idTutor:03d}" if idTutor else '',
                'materia': materia or '',
                'fecha_hora': fecha_hora.strftime("%Y-%m-%d %H:%M") if fecha_hora else '',
                'estado': estado or 'Pendiente',
                'calificacion_dada': calificacion_dada or 0,
                'comentarios': comentarios or ''
            }
            
            # Aplicar filtros
            cumple_materia = not materia_filtro or materia_filtro in (sesion['materia'] or '').lower()
            cumple_estudiante = not estudiante_filtro or estudiante_filtro in (sesion['id_estudiante'] or '').lower()
            cumple_tutor = not tutor_filtro or tutor_filtro in (sesion['id_tutor'] or '').lower()
            
            if cumple_materia and cumple_estudiante and cumple_tutor:
                # Formatear fecha
                try:
                    if sesion['fecha_hora']:
                        fecha_obj = datetime.strptime(sesion['fecha_hora'], "%Y-%m-%d %H:%M")
                        sesion['fecha_formateada'] = fecha_obj.strftime("%d/%m/%Y %H:%M")
                        sesion['fecha_orden'] = fecha_obj.isoformat()
                    else:
                        sesion['fecha_formateada'] = 'Fecha no disponible'
                        sesion['fecha_orden'] = ''
                except (ValueError, KeyError):
                    sesion['fecha_formateada'] = sesion['fecha_hora'] or 'Fecha no disponible'
                    sesion['fecha_orden'] = ''
                
                # Calcular estrellas
                if sesion['estado'] == 'Completada' and sesion['calificacion_dada'] > 0:
                    sesion['estrellas'] = '★' * int(sesion['calificacion_dada'])
                else:
                    sesion['estrellas'] = ''
                
                sesiones_procesadas.append(sesion)
        
        # Ordenar por fecha (más reciente primero)
        sesiones_procesadas.sort(key=lambda x: x.get('fecha_orden', ''), reverse=True)
        
        # Calcular estadísticas
        sesiones_completadas = [s for s in sesiones_procesadas if s['estado'] == 'Completada']
        promedio = sum(s['calificacion_dada'] for s in sesiones_completadas) / len(sesiones_completadas) if sesiones_completadas else 0
        
        return render(request, 'historial_sesiones.html', {
            'sesiones': sesiones_procesadas,
            'total_sesiones': len(sesiones_procesadas),
            'sesiones_completadas': len(sesiones_completadas),
            'promedio_calificaciones': round(promedio, 1),
            'filtros': {
                'materia': materia_filtro,
                'estudiante': estudiante_filtro,
                'tutor': tutor_filtro
            }
        })

    except Exception as e:
        print(f"Error al leer sesiones: {e}")
        return render(request, 'historial_sesiones.html', {
            'error': 'Error al leer las sesiones de la base de datos',
            'sesiones': [],
            'total_sesiones': 0,
            'sesiones_completadas': 0,
            'promedio_calificaciones': 0
        })


# La función que se ejecuta cuando se envía el formulario
@require_POST
def completar_sesion(request):
    try:
        # 1. Obtener los datos del formulario (request.POST)
        id_sesion = request.POST.get('id_sesion')
        calificacion_str = request.POST.get('calificacion')

        # 2. Validar los datos recibidos
        if not id_sesion or not calificacion_str:
            return redirect('historial_sesiones')

        calificacion = int(calificacion_str)
        if not (1 <= calificacion <= 5):
            return redirect('historial_sesiones')

        # 3. Actualizar la sesión en tbl_Sesiones
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Buscar sesión por id_sesion_json
            cursor.execute(
                "SELECT idSesion, estado FROM tbl_Sesiones WHERE id_sesion_json = %s",
                [id_sesion]
            )
            result = cursor.fetchone()
            
            if not result:
                messages.error(request, "Sesión no encontrada.")
                return redirect('historial_sesiones')
            
            idSesion, estado = result
            
            # Solo actualizar si está "Confirmada"
            if estado == 'Confirmada':
                cursor.execute(
                    "UPDATE tbl_Sesiones SET estado = %s, calificacion_dada = %s WHERE idSesion = %s",
                    ['Completada', calificacion, idSesion]
                )
                connection.commit()
                messages.success(request, f"Sesión marcada como completada con calificación {calificacion}.")
            else:
                messages.warning(request, f"La sesión no puede ser completada (estado actual: {estado}).")

        # 4. Redirigir al usuario
        return redirect('historial_sesiones')

    except (ValueError, Exception) as e:
        print(f"Error al completar la sesión: {e}")
        messages.error(request, "Error al procesar la sesión.")
        return redirect('historial_sesiones')


def salir(request):
    return redirect('/')
