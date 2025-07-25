import json
import os
from datetime import datetime

# =========================================================
# CLASES DE ENTIDADES Y ESTRUCTURAS DE DATOS BASE
# =========================================================

class SesionTutoria:
    """Representa una única sesión de tutoría."""
    def __init__(self, id_sesion, id_estudiante, id_tutor, materia, fecha_hora, estado, calificacion_dada=0):
        self.id_sesion = id_sesion
        self.id_estudiante = id_estudiante
        self.id_tutor = id_tutor
        self.materia = materia
        self.fecha_hora = fecha_hora # String 'YYYY-MM-DD HH:MM'
        self.estado = estado  # Ej: "Pendiente", "Confirmada", "Completada", "Cancelada"
        self.calificacion_dada = calificacion_dada # Calificación del estudiante al tutor (1-5)

    def __str__(self):
        return (f"Sesión {self.id_sesion} | Est: {self.id_estudiante} | Tut: {self.id_tutor} | "
                f"Materia: {self.materia} | Fecha: {self.fecha_hora} | Estado: {self.estado} | "
                f"Calificación: {self.calificacion_dada if self.calificacion_dada > 0 else 'N/A'}")

    def to_dict(self):
        """Convierte el objeto SesionTutoria a un diccionario para serialización JSON."""
        return {
            "id_sesion": self.id_sesion,
            "id_estudiante": self.id_estudiante,
            "id_tutor": self.id_tutor,
            "materia": self.materia,
            "fecha_hora": self.fecha_hora,
            "estado": self.estado,
            "calificacion_dada": self.calificacion_dada
        }

# --- Implementación de Lista Enlazada (para historial individual) ---
class NodoListaEnlazada:
    """Un nodo individual para la ListaEnlazada."""
    def __init__(self, dato):
        self.dato = dato  # Espera un objeto de SesionTutoria
        self.siguiente = None

class ListaEnlazada:
    """Implementación manual de una lista enlazada simple para historiales."""
    def __init__(self):
        self.cabeza = None

    def agregar_al_final(self, dato):
        """Añade un nuevo nodo al final de la lista."""
        nuevo_nodo = NodoListaEnlazada(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def mostrar_historial(self):
        """Recorre la lista y muestra los detalles de cada sesión."""
        actual = self.cabeza
        if not actual:
            print("    Historial vacío.")
            return
        while actual:
            s = actual.dato
            print(f"    - {s}")
            actual = actual.siguiente
            
    def to_list(self):
        """Convierte la lista enlazada a una lista Python de diccionarios para serialización."""
        items = []
        actual = self.cabeza
        while actual:
            items.append(actual.dato.to_dict())
            actual = actual.siguiente
        return items


# --- Clases de Usuarios ---
class Usuario:
    """Clase base para Estudiantes y Tutores."""
    def __init__(self, id_usuario, nombre, email, tipo_usuario, historial_tutorias_data=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.tipo_usuario = tipo_usuario
        
        self.historial_tutorias = ListaEnlazada()
        if historial_tutorias_data:
            # Reconstruir la ListaEnlazada a partir de los datos cargados
            for sesion_dict in historial_tutorias_data:
                self.historial_tutorias.agregar_al_final(SesionTutoria(
                    sesion_dict["id_sesion"], sesion_dict["id_estudiante"], 
                    sesion_dict["id_tutor"], sesion_dict["materia"], 
                    sesion_dict["fecha_hora"], sesion_dict["estado"], 
                    sesion_dict["calificacion_dada"]
                ))

    def agregar_a_historial(self, sesion_obj):
        """Agrega una sesión al historial de tutorías del usuario."""
        self.historial_tutorias.agregar_al_final(sesion_obj)

    def __str__(self):
        return f"ID: {self.id_usuario}, Nombre: {self.nombre}, Tipo: {self.tipo_usuario}"


class Estudiante(Usuario):
    """Representa a un estudiante en la plataforma."""
    def __init__(self, id_usuario, nombre, email, nivel_academico, materias_interes, historial_tutorias_data=None):
        super().__init__(id_usuario, nombre, email, "Estudiante", historial_tutorias_data)
        self.nivel_academico = nivel_academico
        self.materias_interes = materias_interes

    def solicitar_tutoria(self, materia, fecha_hora_preferida=None):
        """Prepara una solicitud de tutoría."""
        return {"id_estudiante": self.id_usuario, "materia": materia, "fecha_hora_preferida": fecha_hora_preferida}

    def __str__(self):
        return (f"Estudiante ID: {self.id_usuario} | Nombre: {self.nombre} | Email: {self.email} | "
                f"Nivel: {self.nivel_academico} | Intereses: {', '.join(self.materias_interes)}")

    def to_dict(self):
        """Convierte el objeto Estudiante a un diccionario para serialización JSON."""
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "tipo_usuario": self.tipo_usuario,
            "nivel_academico": self.nivel_academico,
            "materias_interes": self.materias_interes,
            "historial_tutorias": self.historial_tutorias.to_list()
        }


class Tutor(Usuario):
    """Representa a un tutor en la plataforma."""
    def __init__(self, id_usuario, nombre, email, materias_especialidad, calificacion_promedio, disponibilidad, historial_tutorias_data=None):
        super().__init__(id_usuario, nombre, email, "Tutor", historial_tutorias_data)
        self.materias_especialidad = materias_especialidad
        self.calificacion_promedio = calificacion_promedio # Clave para el Árbol Binario
        self.disponibilidad = disponibilidad # {'YYYY-MM-DD HH:MM': 'libre'/'ocupado'}

    def actualizar_disponibilidad(self, fecha_hora, estado):
        """Actualiza el estado de un bloque de tiempo en la disponibilidad del tutor."""
        if fecha_hora in self.disponibilidad:
            self.disponibilidad[fecha_hora] = estado
        else:
            print(f"Advertencia: El horario {fecha_hora} no estaba en la disponibilidad inicial del tutor {self.nombre}. Agregándolo.")
            self.disponibilidad[fecha_hora] = estado # Si no existe, lo añade.

    def __str__(self):
        return (f"Tutor ID: {self.id_usuario} | Nombre: {self.nombre} | Email: {self.email} | "
                f"Especialidad: {', '.join(self.materias_especialidad)} | Calificación: {self.calificacion_promedio:.1f}")

    def to_dict(self):
        """Convierte el objeto Tutor a un diccionario para serialización JSON."""
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "tipo_usuario": self.tipo_usuario,
            "materias_especialidad": self.materias_especialidad,
            "calificacion_promedio": self.calificacion_promedio,
            "disponibilidad": self.disponibilidad,
            "historial_tutorias": self.historial_tutorias.to_list()
        }

# --- Implementación de Cola ---
class Cola:
    """Implementación simple de una cola (FIFO)."""
    def __init__(self, items=None):
        # Asegurarse de que items sea una lista mutable por defecto
        self.items = items if items is not None else []

    def encolar(self, solicitud_obj):
        """Añade un elemento al final de la cola."""
        self.items.append(solicitud_obj)

    def desencolar(self):
        """Retira y devuelve el primer elemento de la cola."""
        if not self.esta_vacia():
            return self.items.pop(0)
        return None # La cola está vacía

    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return len(self.items) == 0

    def tamano(self):
        """Devuelve el número de elementos en la cola."""
        return len(self.items)

    def ver_proximo(self):
        """Devuelve el próximo elemento sin retirarlo."""
        if not self.esta_vacia():
            return self.items[0]
        return None
    
    def to_list(self):
        """Convierte la cola a una lista para serialización."""
        return self.items


# --- Implementación de Árbol Binario de Búsqueda (BST) ---
class NodoArbolBinario:
    """Un nodo individual para el Árbol Binario de Búsqueda."""
    def __init__(self, valor):
        self.valor = valor  # Aquí valor será un objeto Tutor
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    """Implementación de un BST para organizar tutores por calificación."""
    def __init__(self):
        self.raiz = None

    def insertar(self, tutor_obj):
        """Inserta un objeto Tutor en el árbol, ordenado por calificacion_promedio."""
        if self.raiz is None:
            self.raiz = NodoArbolBinario(tutor_obj)
        else:
            self._insertar_recursivo(self.raiz, tutor_obj)

    def _insertar_recursivo(self, nodo_actual, tutor_obj):
        """Método auxiliar recursivo para insertar."""
        if tutor_obj.calificacion_promedio < nodo_actual.valor.calificacion_promedio:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = NodoArbolBinario(tutor_obj)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, tutor_obj)
        else: # Mayor o igual calificación
            if nodo_actual.derecha is None:
                nodo_actual.derecha = NodoArbolBinario(tutor_obj)
            else:
                self._insertar_recursivo(nodo_actual.derecha, tutor_obj)

    def buscar_tutor_por_calificacion(self, calificacion_minima):
        """
        Busca y devuelve una lista de tutores con una calificación promedio
        igual o superior a la calificación_minima.
        """
        resultados = []
        self._buscar_recursivo(self.raiz, calificacion_minima, resultados)
        return resultados

    def _buscar_recursivo(self, nodo, calificacion_minima, resultados):
        """Método auxiliar recursivo para buscar tutores."""
        if nodo:
            # Recorre inorden para encontrar todos los que cumplen la condición
            self._buscar_recursivo(nodo.izquierda, calificacion_minima, resultados)
            if nodo.valor.calificacion_promedio >= calificacion_minima:
                resultados.append(nodo.valor)
            self._buscar_recursivo(nodo.derecha, calificacion_minima, resultados)


    def obtener_todos_los_tutores(self):
        """Devuelve una lista de todos los tutores en el árbol (recorrido inorden)."""
        tutores = []
        self._recorrer_inorden(self.raiz, tutores)
        return tutores

    def _recorrer_inorden(self, nodo, lista_tutores):
        """Método auxiliar para el recorrido inorden."""
        if nodo:
            self._recorrer_inorden(nodo.izquierda, lista_tutores)
            lista_tutores.append(nodo.valor)
            self._recorrer_inorden(nodo.derecha, lista_tutores)

    def eliminar_tutor_por_id(self, id_tutor):
        """
        Reconstruye el árbol con los tutores restantes, excluyendo el tutor con id_tutor.
        Esta es una estrategia simple de eliminación para BSTs no auto-balanceados.
        """
        # Obtener todos los tutores excepto el que se va a eliminar
        tutores_restantes = [t for t in self.obtener_todos_los_tutores() if t.id_usuario != id_tutor]
        
        # Reiniciar el árbol y reinsertar los tutores restantes
        self.raiz = None
        for tutor_obj in tutores_restantes:
            self.insertar(tutor_obj)
        # print(f"Árbol de tutores reconstruido después de eliminar/actualizar a '{id_tutor}'.")


# =========================================================
# CLASE PRINCIPAL DEL SISTEMA
# =========================================================
class PlataformaTutorias:
    """
    Clase principal que orquesta todas las operaciones y estructuras de datos.
    Implementa la versión SIN GRAFOS Y SIN PILAS con persistencia JSON y CRUD completo.
    """
    def __init__(self):
        self.diccionario_estudiantes = {} # {id_estudiante: Estudiante_objeto}
        self.diccionario_tutores = {}     # {id_tutor: Tutor_objeto}
        self.cola_solicitudes = Cola()
        self.arbol_tutores = ArbolBinarioBusqueda() # Organiza tutores por calificación
        # self.pila_vistas_perfil = Pila() # ELIMINADA: Ya no se usa la pila
        self.materias_disponibles = ["Matemáticas", "Física", "Química", "Programación", "Historia", "Literatura", "Biología", "Inglés", "Calculo", "Algoritmos y estructura de datos", "Circuitos electricos", "Bases de datos"] # Ampliadas
        self.historial_general_sesiones = [] # Lista simple de todos los objetos SesionTutoria

        # Nombres de archivos para persistencia
        self.ARCHIVO_ESTUDIANTES = "data/estudiantes.json"
        self.ARCHIVO_TUTORES = "data/tutores.json"
        self.ARCHIVO_SESIONES = "data/sesiones.json"
        self.ARCHIVO_SOLICITUDES = "data/solicitudes.json"
        # self.ARCHIVO_PILAS_VISTAS = "data/pila_vistas.json" # ELIMINADA: Ya no se usa la pila

        # Atributos para el manejo de IDs autoincrementales y persistentes
        self._next_estudiante_id = 1
        self._next_tutor_id = 1
        self.siguiente_id_sesion = 1

        # Asegurarse de que el directorio 'data' existe
        os.makedirs("data", exist_ok=True)

        self._cargar_datos() # Cargar datos al iniciar la plataforma

    def _cargar_datos(self):
        """Carga los datos desde los archivos JSON."""
        print("Cargando datos...")
        try:
            # Cargar estudiantes
            if os.path.exists(self.ARCHIVO_ESTUDIANTES):
                with open(self.ARCHIVO_ESTUDIANTES, 'r') as f:
                    data = json.load(f)
                    for est_dict in data:
                        # Directamente crear el objeto Estudiante
                        estudiante = Estudiante(
                            est_dict["id_usuario"], est_dict["nombre"], est_dict["email"],
                            est_dict["nivel_academico"], est_dict["materias_interes"],
                            est_dict.get("historial_tutorias") # Pasar la lista de dicts para que el constructor la maneje
                        )
                        self.diccionario_estudiantes[estudiante.id_usuario] = estudiante
            
            # Cargar tutores
            if os.path.exists(self.ARCHIVO_TUTORES):
                with open(self.ARCHIVO_TUTORES, 'r') as f:
                    data = json.load(f)
                    for tut_dict in data:
                        # Directamente crear el objeto Tutor
                        tutor = Tutor(
                            tut_dict["id_usuario"], tut_dict["nombre"], tut_dict["email"],
                            tut_dict["materias_especialidad"], tut_dict["calificacion_promedio"],
                            tut_dict["disponibilidad"],
                            tut_dict.get("historial_tutorias") # Pasar la lista de dicts para que el constructor la maneje
                        )
                        self.diccionario_tutores[tutor.id_usuario] = tutor
                        self.arbol_tutores.insertar(tutor) # Reconstruir el árbol de tutores
            
            # Cargar sesiones
            if os.path.exists(self.ARCHIVO_SESIONES):
                with open(self.ARCHIVO_SESIONES, 'r') as f:
                    data = json.load(f)
                    for ses_dict in data:
                        # Directamente crear el objeto SesionTutoria
                        sesion = SesionTutoria(
                            ses_dict["id_sesion"], ses_dict["id_estudiante"], 
                            ses_dict["id_tutor"], ses_dict["materia"], 
                            ses_dict["fecha_hora"], ses_dict["estado"], 
                            ses_dict["calificacion_dada"]
                        )
                        self.historial_general_sesiones.append(sesion)
            
            # Cargar solicitudes (cola)
            if os.path.exists(self.ARCHIVO_SOLICITUDES):
                with open(self.ARCHIVO_SOLICITUDES, 'r') as f:
                    data = json.load(f)
                    self.cola_solicitudes = Cola(items=data) # Se inicializa la cola con la lista cargada

            # Establecer el siguiente ID de sesión, estudiante y tutor basándose en los cargados
            self._next_estudiante_id = self._get_next_id("E", list(self.diccionario_estudiantes.keys()))
            self._next_tutor_id = self._get_next_id("T", list(self.diccionario_tutores.keys()))
            self.siguiente_id_sesion = self._get_next_id("S", [s.id_sesion for s in self.historial_general_sesiones])

            print("Datos cargados exitosamente.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON al cargar datos: {e}. Asegúrese de que los archivos JSON estén bien formados. Iniciando con datos vacíos.")
            self._reset_ids()
        except FileNotFoundError:
            print("Archivos de datos no encontrados. Se iniciará con datos vacíos. (Esto es normal en la primera ejecución)")
            self._reset_ids()
        except Exception as e:
            print(f"Un error inesperado ocurrió al cargar datos: {e}. Iniciando con datos vacíos.")
            self._reset_ids()

    def _reset_ids(self):
        """Reinicia los contadores de ID."""
        self._next_estudiante_id = 1
        self._next_tutor_id = 1
        self.siguiente_id_sesion = 1


    def _get_next_id(self, prefix, existing_ids):
        """Genera el siguiente ID secuencial basado en IDs existentes."""
        if not existing_ids:
            return 1
        
        max_num = 0
        for id_str in existing_ids:
            try:
                # Extraer el número después del prefijo (ej. 'E001' -> 1)
                num_str = id_str[len(prefix):]
                max_num = max(max_num, int(num_str))
            except (ValueError, IndexError):
                continue # Ignorar IDs mal formados
        return max_num + 1

    def _guardar_datos(self):
        """Guarda los datos en los archivos JSON."""
        print("Guardando datos...")
        try:
            # Guardar estudiantes
            with open(self.ARCHIVO_ESTUDIANTES, 'w') as f:
                json.dump([est.to_dict() for est in self.diccionario_estudiantes.values()], f, indent=4)
            
            # Guardar tutores
            with open(self.ARCHIVO_TUTORES, 'w') as f:
                json.dump([tut.to_dict() for tut in self.diccionario_tutores.values()], f, indent=4)
            
            # Guardar sesiones
            with open(self.ARCHIVO_SESIONES, 'w') as f:
                json.dump([ses.to_dict() for ses in self.historial_general_sesiones], f, indent=4)
            
            # Guardar solicitudes (cola)
            with open(self.ARCHIVO_SOLICITUDES, 'w') as f:
                json.dump(self.cola_solicitudes.to_list(), f, indent=4)

            print("Datos guardados exitosamente.")
        except Exception as e:
            print(f"Error al guardar datos: {e}")


    def generar_id_sesion(self):
        """Genera un ID único para cada sesión de tutoría."""
        id_sesion = f"S{self.siguiente_id_sesion:03d}"
        self.siguiente_id_sesion += 1
        return id_sesion

    def registrar_estudiante(self, nombre, email, nivel, materias_interes):
        """
        CRUD: C (Create) - Registra un nuevo estudiante en la plataforma.
        """
        id_est = f"E{self._next_estudiante_id:03d}"
        self._next_estudiante_id += 1
        estudiante = Estudiante(id_est, nombre, email, nivel, materias_interes)
        self.diccionario_estudiantes[id_est] = estudiante
        print(f"Éxito: Estudiante '{nombre}' registrado con ID: {id_est}.")
        self._guardar_datos() # Guardar después de un cambio
        return id_est

    def registrar_tutor(self, nombre, email, especialidad, calificacion, disponibilidad):
        """
        CRUD: C (Create) - Registra un nuevo tutor en la plataforma.
        """
        id_tutor = f"T{self._next_tutor_id:03d}"
        self._next_tutor_id += 1
        tutor = Tutor(id_tutor, nombre, email, especialidad, calificacion, disponibilidad)
        self.diccionario_tutores[id_tutor] = tutor
        self.arbol_tutores.insertar(tutor) # Añade el tutor al árbol por calificación
        print(f"Éxito: Tutor '{nombre}' registrado con ID: {id_tutor}. Calificación promedio: {calificacion:.1f}.")
        self._guardar_datos() # Guardar después de un cambio
        return id_tutor

    def mostrar_perfil_usuario(self, id_usuario):
        """
        CRUD: R (Read) - Muestra el perfil de un usuario.
        """
        usuario = self.diccionario_estudiantes.get(id_usuario)
        if not usuario:
            usuario = self.diccionario_tutores.get(id_usuario)
        
        if usuario:
            print(f"\n--- Perfil de {usuario.nombre} ({usuario.tipo_usuario}) ---")
            print(f"ID: {usuario.id_usuario}")
            print(f"Email: {usuario.email}")
            if usuario.tipo_usuario == "Estudiante":
                print(f"Nivel Académico: {usuario.nivel_academico}")
                print(f"Materias de Interés: {', '.join(usuario.materias_interes)}")
            else: # Es Tutor
                print(f"Materias de Especialidad: {', '.join(usuario.materias_especialidad)}")
                print(f"Calificación Promedio: {usuario.calificacion_promedio:.1f}")
                print("Disponibilidad:")
                if usuario.disponibilidad:
                    for fecha_hora, estado in usuario.disponibilidad.items():
                        print(f"    - {fecha_hora}: {estado}")
                else:
                    print("    No hay disponibilidad registrada.")
            
            print("\n--- Historial de Tutorías Individual ---")
            usuario.historial_tutorias.mostrar_historial()
            
        else:
            print(f"Error: Usuario con ID '{id_usuario}' no encontrado.")

    # ELIMINADO: volver_perfil_anterior() ya no es necesaria sin la pila de vistas.

    def actualizar_estudiante(self, id_estudiante, nuevo_nombre=None, nuevo_email=None, nuevo_nivel=None, nuevas_materias_interes=None):
        """
        CRUD: U (Update) - Actualiza la información de un estudiante existente.
        """
        estudiante = self.diccionario_estudiantes.get(id_estudiante)
        if not estudiante:
            print(f"Error: Estudiante con ID '{id_estudiante}' no encontrado para actualizar.")
            return False

        cambios = False
        if nuevo_nombre is not None:
            estudiante.nombre = nuevo_nombre
            cambios = True
        if nuevo_email is not None:
            estudiante.email = nuevo_email
            cambios = True
        if nuevo_nivel is not None:
            estudiante.nivel_academico = nuevo_nivel
            cambios = True
        if nuevas_materias_interes is not None:
            estudiante.materias_interes = nuevas_materias_interes # Ya se limpian los espacios en main
            cambios = True
        
        if cambios:
            print(f"Éxito: Información del estudiante '{id_estudiante}' actualizada.")
            self._guardar_datos() # Guardar después de un cambio
            return True
        else:
            print("No se proporcionaron nuevos datos para actualizar al estudiante.")
            return False

    def actualizar_tutor(self, id_tutor, nuevo_nombre=None, nuevo_email=None, nuevas_materias_especialidad=None, nueva_calificacion=None, nueva_disponibilidad_dict=None):
        """
        CRUD: U (Update) - Actualiza la información de un tutor existente.
        """
        tutor = self.diccionario_tutores.get(id_tutor)
        if not tutor:
            print(f"Error: Tutor con ID '{id_tutor}' no encontrado para actualizar.")
            return False

        cambios = False
        reinsertar_en_arbol = False 

        if nuevo_nombre is not None:
            tutor.nombre = nuevo_nombre
            cambios = True
        if nuevo_email is not None:
            tutor.email = nuevo_email
            cambios = True
        if nuevas_materias_especialidad is not None:
            tutor.materias_especialidad = nuevas_materias_especialidad # Ya se limpian los espacios en main
            cambios = True
        if nueva_calificacion is not None:
            if nueva_calificacion != tutor.calificacion_promedio:
                tutor.calificacion_promedio = nueva_calificacion
                cambios = True
                reinsertar_en_arbol = True # Marcar para reinsertar si la calificación cambia
        
        if nueva_disponibilidad_dict is not None:
            tutor.disponibilidad.update(nueva_disponibilidad_dict) # Fusiona los diccionarios
            cambios = True
        
        if cambios:
            if reinsertar_en_arbol:
                print(f"La calificación de '{tutor.nombre}' ha cambiado. Reconstruyendo el árbol de tutores.")
                self.arbol_tutores.eliminar_tutor_por_id(id_tutor) # Eliminar y reinsertar
                self.arbol_tutores.insertar(tutor)
            
            print(f"Éxito: Información del tutor '{id_tutor}' actualizada.")
            self._guardar_datos() # Guardar después de un cambio
            return True
        else:
            print("No se proporcionaron nuevos datos para actualizar al tutor.")
            return False

    def eliminar_estudiante(self, id_estudiante):
        """
        CRUD: D (Delete) - Elimina un estudiante y sus sesiones asociadas.
        """
        if id_estudiante not in self.diccionario_estudiantes:
            print(f"Error: Estudiante con ID '{id_estudiante}' no encontrado para eliminar.")
            return False

        # 1. Eliminar de la cola de solicitudes pendientes
        nueva_cola_solicitudes_items = []
        solicitudes_eliminadas_count = 0
        while not self.cola_solicitudes.esta_vacia():
            solicitud = self.cola_solicitudes.desencolar()
            if solicitud['id_estudiante'] == id_estudiante:
                solicitudes_eliminadas_count += 1
            else:
                nueva_cola_solicitudes_items.append(solicitud)
        self.cola_solicitudes = Cola(nueva_cola_solicitudes_items)
        if solicitudes_eliminadas_count > 0:
            print(f"  {solicitudes_eliminadas_count} solicitudes pendientes del estudiante '{id_estudiante}' eliminadas de la cola.")

        # 2. Eliminar sesiones del historial general (sesiones donde el estudiante es el solicitante)
        sesiones_eliminadas_count = 0
        sesiones_a_mantener = []
        for sesion in self.historial_general_sesiones:
            if sesion.id_estudiante == id_estudiante:
                sesiones_eliminadas_count += 1
            else:
                sesiones_a_mantener.append(sesion)
        self.historial_general_sesiones = sesiones_a_mantener
        if sesiones_eliminadas_count > 0:
            print(f"  {sesiones_eliminadas_count} sesiones de tutoría asociadas al estudiante '{id_estudiante}' eliminadas del historial general.")
        
        # 3. Finalmente, eliminar al estudiante del diccionario
        del self.diccionario_estudiantes[id_estudiante]
        print(f"Éxito: Estudiante '{id_estudiante}' eliminado completamente del sistema.")
        self._guardar_datos() # Guardar después de un cambio
        return True

    def eliminar_tutor(self, id_tutor):
        """
        CRUD: D (Delete) - Elimina un tutor y sus sesiones asociadas.
        """
        tutor = self.diccionario_tutores.get(id_tutor)
        if not tutor:
            print(f"Error: Tutor con ID '{id_tutor}' no encontrado para eliminar.")
            return False

        # 1. Eliminar sesiones del historial general (sesiones donde el tutor es el asignado)
        sesiones_eliminadas_count = 0
        sesiones_a_mantener = []
        for sesion in self.historial_general_sesiones:
            if sesion.id_tutor == id_tutor:
                sesiones_eliminadas_count += 1
            else:
                sesiones_a_mantener.append(sesion)
        self.historial_general_sesiones = sesiones_a_mantener
        if sesiones_eliminadas_count > 0:
            print(f"  {sesiones_eliminadas_count} sesiones de tutoría asociadas al tutor '{id_tutor}' eliminadas del historial general.")
        
        # 2. Eliminar del Árbol Binario de Búsqueda
        self.arbol_tutores.eliminar_tutor_por_id(id_tutor)
        
        # 3. Finalmente, eliminar al tutor del diccionario
        del self.diccionario_tutores[id_tutor]
        print(f"Éxito: Tutor '{id_tutor}' eliminado completamente del sistema.")
        self._guardar_datos() # Guardar después de un cambio
        return True

    def solicitar_tutoria(self, id_estudiante, materia, fecha_hora_preferida=None):
        """
        Un estudiante envía una solicitud de tutoría, que se encola.
        """
        estudiante = self.diccionario_estudiantes.get(id_estudiante)
        if not estudiante:
            print(f"Error: Estudiante con ID '{id_estudiante}' no registrado.")
            return

        if materia not in self.materias_disponibles:
            print(f"Error: La materia '{materia}' no está disponible para tutorías.")
            return

        # Verificar si la fecha_hora_preferida es válida si se proporciona
        if fecha_hora_preferida:
            try:
                datetime.strptime(fecha_hora_preferida, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Error: Formato de fecha y hora preferida inválido. Use YYYY-MM-DD HH:MM.")
                return

        solicitud = estudiante.solicitar_tutoria(materia, fecha_hora_preferida)
        self.cola_solicitudes.encolar(solicitud)
        print(f"Éxito: Solicitud de tutoría para '{materia}' de '{estudiante.nombre}' encolada.")
        self._guardar_datos() # Guardar después de un cambio
        

    def asignar_tutoria_a_solicitud(self):
        """
        Procesa la siguiente solicitud de la cola y asigna un tutor disponible.
        """
        if self.cola_solicitudes.esta_vacia():
            print("No hay solicitudes de tutoría pendientes en la cola.")
            return

        solicitud = self.cola_solicitudes.desencolar()
        print(f"\nProcesando solicitud de: {solicitud['id_estudiante']} para materia: {solicitud['materia']}...")

        estudiante = self.diccionario_estudiantes.get(solicitud["id_estudiante"])
        if not estudiante:
            print(f"Error: Estudiante {solicitud['id_estudiante']} no encontrado al procesar solicitud. Solicitud descartada.")
            self._guardar_datos() # Guardar porque la cola cambió
            return

        materia_solicitada = solicitud["materia"]
        fecha_hora_pref = solicitud.get("fecha_hora_preferida")

        tutores_calificados = self.arbol_tutores.buscar_tutor_por_calificacion(3.0) # Umbral de 3.0
        
        tutores_disponibles_para_solicitud = []

        # Ordenar tutores por calificación de mayor a menor para priorizar los mejores
        tutores_calificados.sort(key=lambda t: t.calificacion_promedio, reverse=True)

        for tutor_obj in tutores_calificados:
            if materia_solicitada in tutor_obj.materias_especialidad:
                if fecha_hora_pref:
                    if fecha_hora_pref in tutor_obj.disponibilidad and tutor_obj.disponibilidad[fecha_hora_pref] == "libre":
                        tutores_disponibles_para_solicitud.append((tutor_obj, fecha_hora_pref))
                        break # Priorizar la hora preferida y el primer tutor disponible con esa hora
                else: # Si no hay fecha preferida, buscar cualquier hora libre
                    for hora, estado in tutor_obj.disponibilidad.items():
                        if estado == "libre":
                            tutores_disponibles_para_solicitud.append((tutor_obj, hora))
                            break # Encontramos una hora, pasamos al siguiente tutor (ya ordenados por calificación)

        if not tutores_disponibles_para_solicitud:
            print(f"Error: No se encontraron tutores disponibles para '{materia_solicitada}' en este momento o en la hora preferida.")
            # La solicitud fue desencolada, se podría reencolar si se quiere reintentar
            self._guardar_datos() # Guardar porque la cola cambió
            return

        tutor_seleccionado, hora_asignada = tutores_disponibles_para_solicitud[0] # Tomar el mejor tutor disponible

        id_sesion = self.generar_id_sesion()
        nueva_sesion = SesionTutoria(
            id_sesion, 
            estudiante.id_usuario, 
            tutor_seleccionado.id_usuario, 
            materia_solicitada, 
            hora_asignada, 
            "Confirmada" # Estado inicial de la sesión
        )

        # Actualizar los historiales individuales de estudiante y tutor
        estudiante.agregar_a_historial(nueva_sesion)
        tutor_seleccionado.agregar_a_historial(nueva_sesion)
        tutor_seleccionado.actualizar_disponibilidad(hora_asignada, "ocupado") # Estado 'ocupado'

        self.historial_general_sesiones.append(nueva_sesion)

        print(f"¡Tutoría asignada con éxito!")
        print(f"  ID Sesión: {nueva_sesion.id_sesion}")
        print(f"  Estudiante: {estudiante.nombre} (ID: {estudiante.id_usuario})")
        print(f"  Tutor: {tutor_seleccionado.nombre} (ID: {tutor_seleccionado.id_usuario})")
        print(f"  Materia: {nueva_sesion.materia} | Fecha/Hora: {nueva_sesion.fecha_hora}")
        self._guardar_datos() # Guardar después de un cambio

    def completar_sesion(self, id_sesion, calificacion):
        """
        Marca una sesión como completada y registra la calificación.
        """
        sesion_encontrada = None
        for sesion in self.historial_general_sesiones:
            if sesion.id_sesion == id_sesion:
                sesion_encontrada = sesion
                break

        if sesion_encontrada:
            if sesion_encontrada.estado == "Completada":
                print(f"Advertencia: La sesión {id_sesion} ya ha sido marcada como completada.")
                return False

            sesion_encontrada.estado = "Completada"
            sesion_encontrada.calificacion_dada = calificacion
            print(f"Éxito: Sesión {id_sesion} marcada como 'Completada' y calificada con {calificacion} puntos.")
            
            # Opcional: Recalcular calificación promedio del tutor (más robusto)
            tutor = self.diccionario_tutores.get(sesion_encontrada.id_tutor)
            if tutor:
                # Encuentra todas las calificaciones para este tutor
                calificaciones_tutor = []
                for sesion in self.historial_general_sesiones:
                    if sesion.id_tutor == tutor.id_usuario and sesion.calificacion_dada > 0:
                        calificaciones_tutor.append(sesion.calificacion_dada)
                
                if calificaciones_tutor:
                    nuevo_promedio = sum(calificaciones_tutor) / len(calificaciones_tutor)
                    if tutor.calificacion_promedio != nuevo_promedio:
                        tutor.calificacion_promedio = nuevo_promedio
                        # Reinsertar en el árbol si el promedio cambió para mantener el orden
                        self.arbol_tutores.eliminar_tutor_por_id(tutor.id_usuario) # Eliminar y reinsertar
                        self.arbol_tutores.insertar(tutor)
                        print(f"Calificación promedio del tutor '{tutor.nombre}' actualizada a {tutor.calificacion_promedio:.1f}.")
                else:
                    tutor.calificacion_promedio = 0.0 # Si no hay calificaciones, el promedio es 0
                    print(f"Calificación promedio del tutor '{tutor.nombre}' restablecida a 0.0.")

            self._guardar_datos() # Guardar después de un cambio
            return True
        else:
            print(f"Error: Sesión con ID '{id_sesion}' no encontrada.")
            return False

    def mostrar_historial_general_sesiones(self):
        """Muestra todas las sesiones de tutoría completadas en la plataforma."""
        if not self.historial_general_sesiones:
            print("\nNo hay sesiones en el historial general.")
            return
        
        print("\n--- Historial General de Sesiones de Tutoría ---")
        for sesion in self.historial_general_sesiones:
            print(sesion)

    def listar_estudiantes(self):
        """Muestra un listado de todos los estudiantes registrados."""
        if not self.diccionario_estudiantes:
            print("\nNo hay estudiantes registrados.")
            return
        print("\n--- Listado de Estudiantes ---")
        for est in self.diccionario_estudiantes.values():
            print(est)

    def listar_tutores(self):
        """Muestra un listado de todos los tutores registrados."""
        if not self.diccionario_tutores:
            print("\nNo hay tutores registrados.")
            return
        print("\n--- Listado de Tutores ---")
        # Se podría usar self.arbol_tutores.obtener_todos_los_tutores() para obtenerlos ordenados
        for tut in self.arbol_tutores.obtener_todos_los_tutores(): # Listar desde el árbol para que salgan ordenados
            print(tut)

    def listar_solicitudes_pendientes(self):
        """Muestra las solicitudes pendientes en la cola."""
        if self.cola_solicitudes.esta_vacia():
            print("\nNo hay solicitudes de tutoría pendientes.")
            return
        print("\n--- Solicitudes de Tutoría Pendientes ---")
        for i, solicitud in enumerate(self.cola_solicitudes.items):
            print(f"  {i+1}. Estudiante ID: {solicitud['id_estudiante']}, Materia: {solicitud['materia']}", end="")
            if solicitud['fecha_hora_preferida']:
                print(f", Preferencia: {solicitud['fecha_hora_preferida']}")
            else:
                print("")