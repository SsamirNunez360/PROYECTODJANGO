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

        # Redirigir según el tipo
        if resultado.tipo == "tutor":
            return redirect("tutores_perfil")
        else:  # "estudiante"
            return redirect("estudiantes_perfil")

    # GET → mostrar login
    return render(request, "login.html")



def registrar_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        nivel = request.POST.get('nivel_academico')
        materias = request.POST.getlist('materias_interes') 

        # Cargar el archivo existente
        ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'estudiantes.json')
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                estudiantes_data = json.load(f)
        except FileNotFoundError:
            estudiantes_data = []

        # Generar nuevo ID automático
        nuevo_id = f"E{len(estudiantes_data)+1:03d}"

        # Crear objeto Estudiante
        nuevo_estudiante = Estudiante(
            id_usuario=nuevo_id,
            nombre=nombre,
            email=email,
            nivel_academico=nivel,
            materias_interes=materias
        )

        # Agregar y guardar en JSON
        estudiantes_data.append(nuevo_estudiante.to_dict())
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(estudiantes_data, f, indent=4, ensure_ascii=False)

        return redirect('estudiantes_perfil')

    return render(request, 'registrar_estudiante.html')


def editar_estudiante(request, id_estudiante):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'estudiantes.json')

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            estudiantes = json.load(f)
    except FileNotFoundError:
        messages.error(request, "No se encontró el archivo de estudiantes.")
        return redirect('estudiantes_perfil')

    estudiante = next((e for e in estudiantes if e['id_usuario'] == id_estudiante), None)
    if not estudiante:
        messages.error(request, "Estudiante no encontrado.")
        return redirect('estudiantes_perfil')

    if request.method == 'POST':
        estudiante['nombre'] = request.POST.get('nombre')
        estudiante['email'] = request.POST.get('email')
        estudiante['nivel_academico'] = request.POST.get('nivel_academico')
        estudiante['materias_interes'] = request.POST.getlist('materias_interes')

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(estudiantes, f, indent=4, ensure_ascii=False)

        messages.success(request, "Estudiante actualizado correctamente.")
        return redirect('estudiantes_perfil')

    return render(request, 'editar_estudiante.html', {'estudiante': estudiante})


def eliminar_estudiante(request, id_estudiante):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'estudiantes.json')

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            estudiantes = json.load(f)
    except FileNotFoundError:
        estudiantes = []

    nuevos_estudiantes = [e for e in estudiantes if e['id_usuario'] != id_estudiante]

    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(nuevos_estudiantes, f, indent=4, ensure_ascii=False)

    messages.success(request, "Estudiante eliminado correctamente.")
    return redirect('estudiantes_perfil')




def solicitar_tutoria(request):
    if request.method == 'POST':
        # Ruta exacta corregida (tutoria/mysite/mysite/data/)
        DATA_DIR = Path(settings.BASE_DIR) / 'mysite' / 'data'  # ¡Ajustado!
        DATA_DIR.mkdir(exist_ok=True)  # Crea solo si no existe

        archivo_json = DATA_DIR / 'solicitudes.json'

        # Obtener y formatear la fecha
        fecha_hora_raw = request.POST.get('fecha_hora_preferida')
        try:
            # Convierte el string con T a objeto datetime y lo formatea con espacio
            fecha_hora_obj = datetime.strptime(fecha_hora_raw, "%Y-%m-%dT%H:%M")
            fecha_hora_str = fecha_hora_obj.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            # Si no coincide el formato, usa el string reemplazando la T
            fecha_hora_str = fecha_hora_raw.replace("T", " ")

        # Crear el diccionario de la nueva solicitud
        nueva_solicitud = {
            "id_estudiante": request.POST.get('id_estudiante'),
            "materia": request.POST.get('materia'),
            "fecha_hora_preferida": fecha_hora_str
        }

        # Cargar datos existentes o lista vacía
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                solicitudes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            solicitudes = []

        # Guardar la nueva solicitud
        solicitudes.append(nueva_solicitud)
        
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(solicitudes, f, indent=4, ensure_ascii=False)

        return redirect('home')  # Cambia 'home' si usas otra vista

    return render(request, 'solicitud_tutoria.html')



def listar_solicitudes(request):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'solicitudes.json')

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            solicitudes = json.load(archivo)
    except FileNotFoundError:
        solicitudes = []
    except json.JSONDecodeError:
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
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'tutores.json')

    subject = request.GET.get('subject', '').strip()
    normalized_subject = normalize(subject)

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            tutores = json.load(archivo)
    except FileNotFoundError:
        tutores = []

    # Filtrar tutores que tengan la materia
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
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'estudiantes.json')

    subject = request.GET.get('subject', '').strip()
    normalized_subject = normalize(subject)

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            estudiantes = json.load(archivo)
    except FileNotFoundError:
        estudiantes = []

    # Filtrar estudiantes que tengan la materia en materias_interes
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
    # Ruta al archivo sesiones.json
    ruta_archivo = os.path.join(settings.BASE_DIR, 'mysite', 'data', 'sesiones.json')
    
    # Obtener parámetros de filtrado
    materia_filtro = request.GET.get('materia', '').strip().lower()
    estudiante_filtro = request.GET.get('estudiante', '').strip().lower()
    tutor_filtro = request.GET.get('tutor', '').strip().lower()

    try:
        # Leer archivo JSON
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            sesiones = json.load(archivo)
            
            # Procesar cada sesión
            sesiones_procesadas = []
            for sesion in sesiones:
                # Aplicar filtros
                cumple_materia = not materia_filtro or materia_filtro in sesion.get('materia', '').lower()
                cumple_estudiante = not estudiante_filtro or estudiante_filtro in sesion.get('id_estudiante', '').lower()
                cumple_tutor = not tutor_filtro or tutor_filtro in sesion.get('id_tutor', '').lower()
                
                if cumple_materia and cumple_estudiante and cumple_tutor:
                    # Formatear fecha
                    try:
                        fecha_obj = datetime.strptime(sesion['fecha_hora'], "%Y-%m-%d %H:%M")
                        sesion['fecha_formateada'] = fecha_obj.strftime("%d/%m/%Y %H:%M")
                        sesion['fecha_orden'] = fecha_obj.isoformat()
                    except (ValueError, KeyError):
                        sesion['fecha_formateada'] = sesion.get('fecha_hora', 'Fecha no disponible')
                        sesion['fecha_orden'] = ''
                    
                    # Calcular estrellas
                    if sesion.get('estado') == 'Completada' and sesion.get('calificacion_dada', 0) > 0:
                        sesion['estrellas'] = '★' * int(sesion['calificacion_dada'])
                    else:
                        sesion['estrellas'] = ''
                    
                    sesiones_procesadas.append(sesion)
            
            # Ordenar por fecha (más reciente primero)
            sesiones_procesadas.sort(key=lambda x: x.get('fecha_orden', ''), reverse=True)
            
            # Calcular estadísticas
            sesiones_completadas = [s for s in sesiones_procesadas if s.get('estado') == 'Completada']
            promedio = sum(s.get('calificacion_dada', 0) for s in sesiones_completadas) / len(sesiones_completadas) if sesiones_completadas else 0
            
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
    
    except FileNotFoundError:
        return render(request, 'historial_sesiones.html', {
            'error': 'El archivo de sesiones no fue encontrado',
            'sesiones': [],
            'total_sesiones': 0,
            'sesiones_completadas': 0,
            'promedio_calificaciones': 0
        })
    except json.JSONDecodeError:
        return render(request, 'historial_sesiones.html', {
            'error': 'Error al leer el archivo de sesiones',
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
            # Puedes manejar este error de forma más elegante si lo deseas
            return redirect('historial') # Redirige si faltan datos

        calificacion = int(calificacion_str)
        if not (1 <= calificacion <= 5):
            return redirect('historial') # Redirige si la calificación es inválida

        # 3. Leer y actualizar el archivo JSON
        # Usamos la misma ruta absoluta para asegurar que encontramos el archivo
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_archivo = os.path.join(directorio_base, 'mysite', 'data', 'sesiones.json')

        with open(ruta_archivo, 'r+', encoding='utf-8') as archivo:
            sesiones = json.load(archivo)
            sesion_encontrada = False
            for sesion in sesiones:
                if sesion.get('id_sesion') == id_sesion and sesion.get('estado') == 'Confirmada':
                    sesion['estado'] = 'Completada'
                    sesion['calificacion_dada'] = calificacion
                    sesion_encontrada = True
                    break

            if sesion_encontrada:
                # Volvemos al inicio del archivo para sobrescribirlo
                archivo.seek(0)
                json.dump(sesiones, archivo, indent=4, ensure_ascii=False)
                archivo.truncate() # Cortamos el archivo para evitar datos antiguos

        # 4. Redirigir al usuario
        return redirect('historial_sesiones')

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error al procesar la sesión: {e}")
        return redirect('historial_sesiones')


def salir(request):
    return redirect('/')
