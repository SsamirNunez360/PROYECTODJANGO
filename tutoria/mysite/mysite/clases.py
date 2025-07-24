import json

class Usuario:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre

class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, carrera):
        super().__init__(id_usuario, nombre)
        self.carrera = carrera
        self.historial_sesiones = []

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'carrera': self.carrera,
            'historial_sesiones': [s.id_sesion for s in self.historial_sesiones]
        }

    @staticmethod
    def from_dict(data):
        return Estudiante(data['id_usuario'], data['nombre'], data['carrera'])

class Tutor(Usuario):
    def __init__(self, id_usuario, nombre, materias, calificaciones):
        super().__init__(id_usuario, nombre)
        self.materias = materias
        self.calificaciones = calificaciones
        self.disponibilidad = {m: True for m in materias}
        self.historial_sesiones = []

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'materias': self.materias,
            'calificaciones': self.calificaciones,
            'disponibilidad': self.disponibilidad,
            'historial_sesiones': [s.id_sesion for s in self.historial_sesiones]
        }

    @staticmethod
    def from_dict(data):
        tutor = Tutor(data['id_usuario'], data['nombre'], data['materias'], data['calificaciones'])
        tutor.disponibilidad = data.get('disponibilidad', {m: True for m in data['materias']})
        return tutor

class SesionTutoria:
    def __init__(self, id_sesion, id_solicitud, id_estudiante, id_tutor, materia):
        self.id_sesion = id_sesion
        self.id_solicitud = id_solicitud
        self.id_estudiante = id_estudiante
        self.id_tutor = id_tutor
        self.materia = materia

    def to_dict(self):
        return {
            'id_sesion': self.id_sesion,
            'id_solicitud': self.id_solicitud,
            'id_estudiante': self.id_estudiante,
            'id_tutor': self.id_tutor,
            'materia': self.materia
        }

    @staticmethod
    def from_dict(data):
        return SesionTutoria(
            data['id_sesion'],
            data['id_solicitud'],
            data['id_estudiante'],
            data['id_tutor'],
            data['materia']
        )

class ListaEnlazada:
    def __init__(self):
        self.lista = []

    def agregar_al_final(self, elemento):
        self.lista.append(elemento)

    def obtener_todos(self):
        return self.lista

class ArbolBinarioBusqueda:
    def __init__(self):
        self.elementos = []

    def insertar(self, tutor):
        self.elementos.append(tutor)

class TutorIAConnectPro:
    def __init__(self):
        self.estudiantes = {}
        self.tutores = {}
        self.lista_estudiantes = []
        self.lista_tutores = []
        self.arbol_tutores = ArbolBinarioBusqueda()
        self.historial_global_sesiones = ListaEnlazada()
        self.next_solicitud_id = 1
        self.next_sesion_id = 1
        
    def registrar_estudiante(self, id_estudiante, nombre, carrera):
        estudiante = Estudiante(id_estudiante, nombre, carrera)
        self.estudiantes[id_estudiante] = estudiante
        self.lista_estudiantes.append(estudiante)
        
    def registrar_tutor(self, id_tutor, nombre, materias, calificaciones):
        tutor = Tutor(id_tutor, nombre, materias, calificaciones)
        self.lista_tutores.append(tutor)

    def guardar_datos(self, archivo='datos.json'):
        data = {
            'estudiantes': [e.to_dict() for e in self.lista_estudiantes],
            'tutores': [t.to_dict() for t in self.lista_tutores],
            'sesiones': [s.to_dict() for s in self.historial_global_sesiones.obtener_todos()],
            'next_solicitud_id': self.next_solicitud_id,
            'next_sesion_id': self.next_sesion_id
        }
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def cargar_datos(self, archivo='datos.json'):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.estudiantes = {}
            self.lista_estudiantes = []
            for est_data in data['estudiantes']:
                est = Estudiante.from_dict(est_data)
                self.estudiantes[est.id_usuario] = est
                self.lista_estudiantes.append(est)

            self.tutores = {}
            self.lista_tutores = []
            self.arbol_tutores = ArbolBinarioBusqueda()
            for tut_data in data['tutores']:
                tut = Tutor.from_dict(tut_data)
                self.tutores[tut.id_usuario] = tut
                self.lista_tutores.append(tut)
                self.arbol_tutores.insertar(tut)

            self.historial_global_sesiones = ListaEnlazada()
            sesiones_dict = {}
            for ses_data in data['sesiones']:
                sesion = SesionTutoria.from_dict(ses_data)
                sesiones_dict[sesion.id_sesion] = sesion
                self.historial_global_sesiones.agregar_al_final(sesion)

            for est in self.lista_estudiantes:
                est.historial_sesiones = [sesiones_dict[sid] for sid in est.to_dict()['historial_sesiones'] if sid in sesiones_dict]

            for tut in self.lista_tutores:
                tut.historial_sesiones = [sesiones_dict[sid] for sid in tut.to_dict()['historial_sesiones'] if sid in sesiones_dict]

            self.next_solicitud_id = data.get('next_solicitud_id', 1)
            self.next_sesion_id = data.get('next_sesion_id', 1)

        except FileNotFoundError:
            print("Archivo de datos no encontrado. Se iniciará con datos vacíos.")
