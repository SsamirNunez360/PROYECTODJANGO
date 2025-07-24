# ESTRUCTURAS DE DATOS PERSONALIZADAS

class Nodo:
    # Nodo para listas enlazadas.
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    # Lista enlazada simple, usada para almacenar historiales de sesiones.
    def __init__(self):
        self.primero = None

    def agregar_al_final(self, dato):
        nuevo = Nodo(dato)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def mostrar_historial(self):
        return [str(dato) for dato in self]


class Cola:
    # Cola simple FIFO para manejar solicitudes de tutoría.
    def __init__(self):
        self.items = []

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)

    def esta_vacia(self):
        return len(self.items) == 0

    def tamano(self):
        return len(self.items)

    def ver_primero(self):
        if not self.esta_vacia():
            return self.items[0]


# CLASES DE ENTIDADES BASE

class Usuario:
    # Representa un usuario genérico del sistema.
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.historial_sesiones = ListaEnlazada()

    def __str__(self):
        return f"{self.nombre} (ID: {self.id_usuario})"


class Estudiante(Usuario):
    # Representa un estudiante, hereda de Usuario.
    def __init__(self, id_usuario, nombre, carrera):
        super().__init__(id_usuario, nombre)
        self.carrera = carrera


class Tutor(Usuario):
    # Representa un tutor, hereda de Usuario.
    def __init__(self, id_usuario, nombre, especialidad, calificaciones_por_materia):
        super().__init__(id_usuario, nombre)
        self.especialidad = especialidad  # Lista de materias
        self.calificaciones_por_materia = calificaciones_por_materia  # Dict con notas por materia
        self.disponibilidad = {}  # Dict {'2025-07-23 10:00': 'disponible' / 'ocupado'}

    @property
    def calificacion_promedio_general(self):
        # Calcula el promedio general de todas las calificaciones.
        if not self.calificaciones_por_materia:
            return 0
        return sum(self.calificaciones_por_materia.values()) / len(self.calificaciones_por_materia)


class SolicitudTutoria:
    # Representa una solicitud de tutoría.
    def __init__(self, id_solicitud, id_estudiante, materia, fecha_preferida, hora_preferida):
        self.id_solicitud = id_solicitud
        self.id_estudiante = id_estudiante
        self.materia = materia
        self.fecha_preferida = fecha_preferida
        self.hora_preferida = hora_preferida
        self.estado = "pendiente"  # otros posibles: 'asignada', 'rechazada'


class SesionTutoria:
    # Representa una sesión de tutoría ya asignada.
    def __init__(self, id_sesion, id_estudiante, id_tutor, materia, fecha, hora, duracion, estado):
        self.id_sesion = id_sesion
        self.id_estudiante = id_estudiante
        self.id_tutor = id_tutor
        self.materia = materia
        self.fecha = fecha
        self.hora = hora
        self.duracion = duracion  # en minutos
        self.estado = estado  # 'programada', 'completada', etc.

    def __str__(self):
        return f"Sesión {self.id_sesion}: {self.materia} con Tutor {self.id_tutor} el {self.fecha} a las {self.hora}"


# ÁRBOL BINARIO DE BÚSQUEDA

class NodoBST:
    # Nodo del Árbol Binario de Búsqueda que contiene un objeto Tutor.
    def __init__(self, tutor):
        self.tutor = tutor
        self.izquierda = None
        self.derecha = None


class ArbolBinarioBusqueda:
    # Árbol Binario de Búsqueda basado en la calificación promedio general del tutor.
    def __init__(self):
        self.raiz = None

    def insertar(self, tutor):
        # Inserta un tutor en el árbol basado en su calificación promedio general.
        if self.raiz is None:
            self.raiz = NodoBST(tutor)
        else:
            self._insertar_recursivo(self.raiz, tutor)

    def _insertar_recursivo(self, nodo, tutor):
        if tutor.calificacion_promedio_general < nodo.tutor.calificacion_promedio_general:
            if nodo.izquierda is None:
                nodo.izquierda = NodoBST(tutor)
            else:
                self._insertar_recursivo(nodo.izquierda, tutor)
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoBST(tutor)
            else:
                self._insertar_recursivo(nodo.derecha, tutor)

    def obtener_tutores_ordenados(self):
        # Devuelve una lista de tutores ordenados de mayor a menor por calificación.
        resultado = []
        self._inorden_inverso(self.raiz, resultado)
        return resultado

    def _inorden_inverso(self, nodo, resultado):
        if nodo is not None:
            self._inorden_inverso(nodo.derecha, resultado)
            resultado.append(nodo.tutor)
            self._inorden_inverso(nodo.izquierda, resultado)
