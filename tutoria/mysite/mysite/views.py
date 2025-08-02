# mysite/views.py

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
# Django
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Dominio de la plataforma de tutorías (definido en clases.py)
# Si este archivo (views.py) y clases.py están en la MISMA app:
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

        with open('ruta/a/tu/archivo/usuarios.json', 'r') as f:
            usuarios = json.load(f)

        usuario = next((u for u in usuarios if u['email'] == email and u['password'] == password), None)

        if usuario:
            # Usuario autenticado
            request.session['usuario'] = usuario  # Guardar info en sesión
            return redirect('home')  # O donde quieras redirigir
        else:
            messages.error(request, 'Email o contraseña incorrectos')

    return render(request, 'login.html')


def registrar_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        nivel = request.POST.get('nivel_academico')
        materias = request.POST.getlist('materias_interes')  # Asegúrate que en HTML uses name="materias_interes"

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

        return redirect('estudiantes_perfil')  # Ajusta según la URL que tengas

    return render(request, 'registrar_estudiante.html')


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

    # Filtrar tutores que tengan la materia (normalizada)
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

    # Filtrar estudiantes que tengan la materia (normalizada) en materias_interes
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


# Ejemplo de vista de login
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
            return redirect('dashboard_basico')
    
    return render(request, 'login.html')

# Ejemplo de vista de registro
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


# Se mantiene la función para mostrar el formulario
def registrar_estudiante_get(request):
    return render(request, 'registrar_estudiante.html')

def listar_estudiante(request):
    return render(request, 'listar_estudiante.html')

def registrar_tutor(request):
    """
    Vista que maneja el registro de un nuevo tutor.
    """
    if request.method == 'POST':
        # 1. Extraer los datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        materias_especialidad_str = request.POST.get('materias_especialidad')
        
        # 2. Procesar las materias de especialidad (separar por coma)
        materias_especialidad = [m.strip() for m in materias_especialidad_str.split(',')]
        
        # 3. Llamar a la lógica de negocio para registrar al tutor
        plataforma = PlataformaTutorias() # Asumiendo que tu clase PlataformaTutorias tiene un método para esto
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

def solicitar_tutoria(request):
    return render(request, 'solicitar_tutoria.html')

def listar_solicitudes(request):
    return render(request, 'listar_solicitudes.html')

def asignar_tutoria(request):
    return render(request, 'asignar_tutoria.html')

def completar_sesion(request):
    return render(request, 'completar_sesion.html')

def historial_sesiones(request):
    return render(request, 'historial_sesiones.html')

def salir(request):
    return redirect('/')

########