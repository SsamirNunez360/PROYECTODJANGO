class SesionTutoria:
    def __init__(self, id_sesion, id_estudiante, id_tutor, materia, fecha_hora, estado, calificacion_dada=0):
        self.id_sesion = id_sesion
        self.id_estudiante = id_estudiante
        self.id_tutor = id_tutor
        self.materia = materia
        self.fecha_hora = fecha_hora
        self.estado = estado
        self.calificacion_dada = calificacion_dada


class NodoListaEnlazada:
    def __init__(self, dato):
        self.dato = dato  # Espera un objeto de SesionTutoria
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar_al_final(self, dato):
        nuevo_nodo = NodoListaEnlazada(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def mostrar_historial(self):
        actual = self.cabeza
        while actual:
            s = actual.dato
            print(f"Sesión {s.id_sesion} | Estudiante: {s.id_estudiante} | Tutor: {s.id_tutor} | Estado: {s.estado}")
            actual = actual.siguiente


class Usuario:
    def __init__(self, id_usuario, nombre, email, tipo_usuario):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.tipo_usuario = tipo_usuario
        self.historial_tutorias = ListaEnlazada()

    def agregar_a_historial(self, sesion_obj):
        self.historial_tutorias.agregar_al_final(sesion_obj)


class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, email, nivel_academico, materias_interes):
        super().__init__(id_usuario, nombre, email, "Estudiante")
        self.nivel_academico = nivel_academico
        self.materias_interes = materias_interes

    def solicitar_tutoria(self, materia):
        return {"id_estudiante": self.id_usuario, "materia": materia}


class Tutor(Usuario):
    def __init__(self, id_usuario, nombre, email, materias_especialidad, calificacion_promedio, disponibilidad):
        super().__init__(id_usuario, nombre, email, "Tutor")
        self.materias_especialidad = materias_especialidad
        self.calificacion_promedio = calificacion_promedio
        self.disponibilidad = disponibilidad

    def actualizar_disponibilidad(self, fecha_hora, estado):
        self.disponibilidad[fecha_hora] = estado


class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, solicitud_obj):
        self.items.append(solicitud_obj)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def esta_vacia(self):
        return len(self.items) == 0


class Pila:
    def __init__(self):
        self.items = []

    def apilar(self, id_usuario):
        self.items.append(id_usuario)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None

    def esta_vacia(self):
        return len(self.items) == 0

    def ver_cima(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

class NodoArbolBinario:
    def __init__(self, valor):
        self.valor = valor  # Objeto Tutor
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, tutor_obj):
        if self.raiz is None:
            self.raiz = NodoArbolBinario(tutor_obj)
        else:
            self._insertar_recursivo(self.raiz, tutor_obj)

    def _insertar_recursivo(self, nodo_actual, tutor_obj):
        if tutor_obj.calificacion_promedio < nodo_actual.valor.calificacion_promedio:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = NodoArbolBinario(tutor_obj)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, tutor_obj)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = NodoArbolBinario(tutor_obj)
            else:
                self._insertar_recursivo(nodo_actual.derecha, tutor_obj)

    def buscar_tutor_por_calificacion(self, calificacion_minima):
        resultados = []
        self._buscar_recursivo(self.raiz, calificacion_minima, resultados)
        return resultados

    def _buscar_recursivo(self, nodo, calificacion_minima, resultados):
        if nodo:
            if nodo.valor.calificacion_promedio >= calificacion_minima:
                resultados.append(nodo.valor)
            self._buscar_recursivo(nodo.izquierda, calificacion_minima, resultados)
            self._buscar_recursivo(nodo.derecha, calificacion_minima, resultados)


class PlataformaTutorias:
    def __init__(self):
        self.diccionario_estudiantes = {}
        self.diccionario_tutores = {}
        self.cola_solicitudes = Cola()
        self.arbol_tutores = ArbolBinarioBusqueda()
        self.pila_vistas_perfil = Pila()
        self.materias_disponibles = ["Matemáticas", "Física", "Química", "Programación"]
        self.historial_general_sesiones = []
        self.siguiente_id_sesion = 1

    def generar_id_sesion(self):
        id_sesion = f"S{self.siguiente_id_sesion:03}"
        self.siguiente_id_sesion += 1
        return id_sesion

    def registrar_estudiante(self, nombre, email, nivel, materias_interes):
        id_est = f"E{len(self.diccionario_estudiantes)+1:03}"
        estudiante = Estudiante(id_est, nombre, email, nivel, materias_interes)
        self.diccionario_estudiantes[id_est] = estudiante
        return id_est

    def registrar_tutor(self, nombre, email, especialidad, calificacion, disponibilidad):
        id_tutor = f"T{len(self.diccionario_tutores)+1:03}"
        tutor = Tutor(id_tutor, nombre, email, especialidad, calificacion, disponibilidad)
        self.diccionario_tutores[id_tutor] = tutor
        self.arbol_tutores.insertar(tutor)
        return id_tutor

    def mostrar_perfil_usuario(self, id_usuario):
        usuario = self.diccionario_estudiantes.get(id_usuario) or self.diccionario_tutores.get(id_usuario)
        if usuario:
            self.pila_vistas_perfil.apilar(id_usuario)
            print(f"\n--- Perfil de {usuario.nombre} ---")
            print(f"ID: {usuario.id_usuario} | Tipo: {usuario.tipo_usuario}")
            print(f"Email: {usuario.email}")
        else:
            print("Usuario no encontrado.")

    def volver_perfil_anterior(self):
        id_anterior = self.pila_vistas_perfil.desapilar()
        if id_anterior:
            self.mostrar_perfil_usuario(id_anterior)
        else:
            print("No hay perfil anterior.")

    def solicitar_tutoria(self, id_estudiante, materia):
        solicitud = {"id_estudiante": id_estudiante, "materia": materia}
        self.cola_solicitudes.encolar(solicitud)

    def asignar_tutoria_a_solicitud(self):
        solicitud = self.cola_solicitudes.desencolar()
        if not solicitud:
            print("No hay solicitudes pendientes.")
            return

        estudiante = self.diccionario_estudiantes.get(solicitud["id_estudiante"])
        if not estudiante:
            print("Estudiante no encontrado.")
            return

        posibles_tutores = self.arbol_tutores.buscar_tutor_por_calificacion(3.0)  # Cambiar si se quiere mínimo diferente
        tutores_disponibles = []

        for tutor in posibles_tutores:
            for hora, estado in tutor.disponibilidad.items():
                if solicitud["materia"] in tutor.materias_especialidad and estado == "libre":
                    tutores_disponibles.append((tutor, hora))
                    break

        if not tutores_disponibles:
            print("No se encontraron tutores disponibles para esa materia.")
            return

        tutor, hora = tutores_disponibles[0]
        id_sesion = self.generar_id_sesion()
        sesion = SesionTutoria(id_sesion, estudiante.id_usuario, tutor.id_usuario, solicitud["materia"], hora, "Pendiente")
        estudiante.agregar_a_historial(sesion)
        tutor.agregar_a_historial(sesion)
        tutor.actualizar_disponibilidad(hora, "ocupado")
        self.historial_general_sesiones.append(sesion)
        print(f"Tutoría asignada: {id_sesion} con {tutor.nombre} a las {hora}")

    def completar_sesion(self, id_sesion, calificacion):
        for sesion in self.historial_general_sesiones:
            if sesion.id_sesion == id_sesion:
                sesion.estado = "Completada"
                sesion.calificacion_dada = calificacion
                print(f"Sesión {id_sesion} completada y calificada con {calificacion}")
                return
        print("Sesión no encontrada.")


