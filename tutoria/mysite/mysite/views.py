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


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with open('data/usuarios.json', 'r') as f:
            usuarios = json.load(f)

        usuario = next((u for u in usuarios if u['email'] == email and u['password'] == password), None)

        if usuario:
            # Usuario autenticado
            request.session['usuario'] = usuario  # Guardar info en sesión
            return redirect('home')
        else:
            messages.error(request, 'Email o contraseña incorrectos')

    return render(request, 'login.html')


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





def solicitar_tutoria(request):
    if request.method == 'POST':
        # Ruta exacta corregida (tutoria/mysite/mysite/data/)
        DATA_DIR = Path(settings.BASE_DIR) / 'mysite' / 'data'  # ¡Ajustado!
        DATA_DIR.mkdir(exist_ok=True)  # Crea solo si no existe

        archivo_json = DATA_DIR / 'solicitudes.json'

        # Obtener datos del formulario
        nueva_solicitud = {
            "id_estudiante": request.POST.get('id_estudiante'),
            "materia": request.POST.get('materia'),
            "fecha_hora_preferida": request.POST.get('fecha_hora_preferida')
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



def iniciar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        plataforma = PlataformaTutorias()
        resultado = plataforma.iniciar_sesion(email, password)
        
        if not resultado:
            messages.error(request, 'Credenciales incorrectas')
            return render(request, 'login.html')
        
        # Guardar en sesión según el tipo de usuario
        request.session['user_type'] = resultado['tipo']
        request.session['user_email'] = email
        
        if resultado['tipo'] == 'estudiante':
            request.session['user_id'] = resultado['objeto'].id_usuario
            return redirect('dashboard_estudiante')
        elif resultado['tipo'] == 'tutor':
            request.session['user_id'] = resultado['objeto'].id_usuario
            return redirect('dashboard_tutor')
        else:
            return redirect('home')
    
    return render(request, 'login.html')


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



def salir(request):
    return redirect('/')
