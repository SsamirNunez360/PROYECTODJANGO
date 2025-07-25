import os
from datetime import datetime
from clases import PlataformaTutorias

def mostrar_menu():
    print("\n======================================")
    print("== BIENVENIDO A TutorIAConnectPro ==")
    print("======================================")
    print("\n--- GESTIÓN DE USUARIOS (CRUD) ---")
    print("1. Registrar nuevo Estudiante")        # CREATE (Estudiante)
    print("2. Registrar nuevo Tutor")             # CREATE (Tutor)
    print("3. Ver perfil de Usuario (Estudiante/Tutor)") # READ (Individual)
    print("4. Listar todos los Estudiantes")       # READ (Todos)
    print("5. Listar todos los Tutores")           # READ (Todos)
    print("6. Actualizar información de Usuario (Estudiante/Tutor)") # UPDATE
    print("7. Eliminar Usuario (Estudiante/Tutor)") # DELETE

    print("\n--- GESTIÓN DE TUTORÍAS ---")
    print("8. Enviar solicitud de tutoría")
    print("9. Listar solicitudes pendientes")
    print("10. Asignar siguiente tutoría")
    print("11. Completar sesión de tutoría y calificar")
    print("12. Mostrar historial general de sesiones")

    print("\n13. Salir")
    print("======================================")


def main():
    # Inicializa la plataforma, lo que automáticamente carga los datos.
    plataforma = PlataformaTutorias()

    # --- Líneas de depuración añadidas ---
    print(f"DEBUG: Directorio de trabajo actual: {os.getcwd()}")
    print(f"DEBUG: Archivos de datos esperados en: {os.path.join(os.getcwd(), 'data')}")
    # --- Fin de líneas de depuración ---

    while True:
        mostrar_menu()
        opcion = input("Ingrese su opción: ").strip()

        if opcion == "1": # Registrar Estudiante (CREATE)
            nombre = input("Nombre del estudiante: ").strip()
            email = input("Email: ").strip()
            nivel = input("Nivel académico: ").strip()
            materias = input("Materias de interés (separadas por coma, ej: Matematicas, Fisica): ").strip()
            materias_list = [m.strip() for m in materias.split(',') if m.strip()]
            if not materias_list:
                print("Advertencia: No se ingresaron materias de interés. El estudiante no podrá solicitar tutorías por materia específica.")
            plataforma.registrar_estudiante(nombre, email, nivel, materias_list)

        elif opcion == "2": # Registrar Tutor (CREATE)
            nombre = input("Nombre del tutor: ").strip()
            email = input("Email: ").strip()
            especialidad = input("Materias de especialidad (separadas por coma, ej: Calculo, Algoritmos): ").strip()
            especialidad_list = [m.strip() for m in especialidad.split(',') if m.strip()]
            if not especialidad_list:
                print("Error: Un tutor debe tener al menos una materia de especialidad.")
                continue

            try:
                calificacion = float(input("Calificación promedio inicial (ej. 4.5, 0 si no tiene): "))
                if not (0.0 <= calificacion <= 5.0):
                    raise ValueError("La calificación debe estar entre 0.0 y 5.0.")
            except ValueError as e:
                print(f"Error en la calificación: {e}. Por favor, ingrese un número válido (0-5).")
                continue
            
            disponibilidad = {}
            print("Ingrese horarios disponibles (formato: YYYY-MM-DD HH:MM), escriba 'fin' para terminar:")
            while True:
                entrada_hora = input("Hora disponible: ").strip()
                if entrada_hora.lower() == "fin":
                    break
                try:
                    datetime.strptime(entrada_hora, "%Y-%m-%d %H:%M") # Validar formato
                    disponibilidad[entrada_hora] = "libre"
                except ValueError:
                    print("Formato de fecha y hora inválido. Use YYYY-MM-DD HH:MM. Intente de nuevo.")
            
            if not disponibilidad:
                print("Advertencia: El tutor no tiene horarios de disponibilidad registrados. No podrá ser asignado automáticamente.")

            plataforma.registrar_tutor(nombre, email, especialidad_list, calificacion, disponibilidad)
        
        elif opcion == "3": # Ver Perfil de Usuario (READ - Individual)
            id_usuario = input("ID de usuario a ver (ej. E001 o T001): ").strip()
            plataforma.mostrar_perfil_usuario(id_usuario)

        elif opcion == "4": # Listar Estudiantes (READ - Todos)
            plataforma.listar_estudiantes()

        elif opcion == "5": # Listar Tutores (READ - Todos)
            plataforma.listar_tutores()

        elif opcion == "6": # Actualizar Usuario (UPDATE)
            print("\n--- Actualizar Información de Usuario ---")
            tipo_usuario = input("¿Desea actualizar un 'estudiante' o un 'tutor'? ").lower().strip()
            
            if tipo_usuario == "estudiante":
                id_est = input("Ingrese el ID del estudiante a actualizar (ej. E001): ").strip()
                estudiante_existente = plataforma.diccionario_estudiantes.get(id_est)
                if estudiante_existente:
                    print(f"\nDatos actuales del estudiante {id_est}: {estudiante_existente}")
                    print("Deje el campo vacío si no desea cambiar el valor.")
                    
                    nuevo_nombre = input(f"Nuevo nombre (actual: {estudiante_existente.nombre}): ").strip() or None
                    nuevo_email = input(f"Nuevo email (actual: {estudiante_existente.email}): ").strip() or None
                    nuevo_nivel = input(f"Nuevo nivel académico (actual: {estudiante_existente.nivel_academico}): ").strip() or None
                    
                    nuevas_materias_str = input(f"Nuevas materias de interés (actual: {', '.join(estudiante_existente.materias_interes)}, separadas por coma): ").strip()
                    materias_list = [m.strip() for m in nuevas_materias_str.split(',') if m.strip()] if nuevas_materias_str else None
                    
                    plataforma.actualizar_estudiante(
                        id_est, 
                        nuevo_nombre,
                        nuevo_email,
                        nuevo_nivel,
                        materias_list
                    )
                else:
                    print(f"Error: Estudiante con ID '{id_est}' no encontrado.")

            elif tipo_usuario == "tutor":
                id_tutor = input("Ingrese el ID del tutor a actualizar (ej. T001): ").strip()
                tutor_existente = plataforma.diccionario_tutores.get(id_tutor)
                if tutor_existente:
                    print(f"\nDatos actuales del tutor {id_tutor}: {tutor_existente}")
                    print("Deje el campo vacío si no desea cambiar el valor.")
                    
                    nuevo_nombre = input(f"Nuevo nombre (actual: {tutor_existente.nombre}): ").strip() or None
                    nuevo_email = input(f"Nuevo email (actual: {tutor_existente.email}): ").strip() or None
                    nuevas_especialidades_str = input(f"Nuevas materias de especialidad (actual: {', '.join(tutor_existente.materias_especialidad)}, separadas por coma): ").strip()
                    nueva_calificacion_str = input(f"Nueva calificación promedio (actual: {tutor_existente.calificacion_promedio:.1f}, ingrese 0-5): ").strip()

                    nuevas_disponibilidades_dict = {}
                    print("\n--- Actualizar Disponibilidad ---")
                    print("Ingrese 'add' para añadir/modificar un horario, o 'fin' para terminar.")
                    print("Formato de horario: YYYY-MM-DD HH:MM (ej. 2025-07-25 10:00)")
                    print("Estados válidos: 'libre', 'ocupado'")

                    while True:
                        accion = input("¿Añadir/Modificar disponibilidad? (add/fin): ").strip().lower()
                        if accion == 'fin':
                            break
                        if accion == 'add':
                            entrada_hora = input("   Fecha/Hora: ").strip()
                            entrada_estado = input("   Estado ('libre'/'ocupado'): ").strip().lower()
                            try:
                                datetime.strptime(entrada_hora, "%Y-%m-%d %H:%M")
                                if entrada_estado in ["libre", "ocupado"]:
                                    nuevas_disponibilidades_dict[entrada_hora] = entrada_estado
                                else:
                                    print("     Estado inválido. Ingrese 'libre' u 'ocupado'.")
                            except ValueError:
                                print("     Formato de fecha y hora inválido. Intente de nuevo.")
                        else:
                            print("Opción inválida. Ingrese 'add' o 'fin'.")


                    especialidades_list = [m.strip() for m in nuevas_especialidades_str.split(',') if m.strip()] if nuevas_especialidades_str else None
                    
                    nueva_calificacion = None
                    if nueva_calificacion_str:
                        try:
                            nueva_calificacion = float(nueva_calificacion_str)
                            if not (0.0 <= nueva_calificacion <= 5.0):
                                raise ValueError("La calificación debe estar entre 0.0 y 5.0.")
                        except ValueError as e:
                            print(f"Error en la calificación: {e}. Dejando la calificación sin cambios.")
                            nueva_calificacion = None # Si hay error, no se actualiza

                    plataforma.actualizar_tutor(
                        id_tutor,
                        nuevo_nombre,
                        nuevo_email,
                        especialidades_list,
                        nueva_calificacion,
                        nuevas_disponibilidades_dict if nuevas_disponibilidades_dict else None
                    )
                else:
                    print(f"Error: Tutor con ID '{id_tutor}' no encontrado.")
            else:
                print("Tipo de usuario inválido. Por favor, ingrese 'estudiante' o 'tutor'.")

        elif opcion == "7": # Eliminar Usuario (DELETE)
            print("\n--- Eliminar Usuario ---")
            tipo_usuario = input("¿Desea eliminar un 'estudiante' o un 'tutor'? ").lower().strip()
            
            if tipo_usuario == "estudiante":
                id_est = input("Ingrese el ID del estudiante a eliminar (ej. E001): ").strip()
                plataforma.eliminar_estudiante(id_est)
            elif tipo_usuario == "tutor":
                id_tutor = input("Ingrese el ID del tutor a eliminar (ej. T001): ").strip()
                plataforma.eliminar_tutor(id_tutor)
            else:
                print("Tipo de usuario inválido. Por favor, ingrese 'estudiante' o 'tutor'.")

        elif opcion == "8": # Enviar solicitud
            id_est = input("ID del estudiante que solicita (ej. E001): ").strip()
            materia = input("Materia para tutoría: ").strip()
            fecha_hora_pref = input("Fecha y hora preferida (YYYY-MM-DD HH:MM) o Enter si no hay preferencia: ").strip()
            if not fecha_hora_pref:
                fecha_hora_pref = None
            
            plataforma.solicitar_tutoria(id_est, materia, fecha_hora_pref)

        elif opcion == "9": # Listar Solicitudes Pendientes
            plataforma.listar_solicitudes_pendientes()

        elif opcion == "10": # Asignar Tutoría
            plataforma.asignar_tutoria_a_solicitud()

        elif opcion == "11": # Completar Sesión
            id_sesion = input("ID de la sesión a completar (ej. S001): ").strip()
            try:
                calificacion = int(input("Calificación dada al tutor (1 a 5): "))
                if not (1 <= calificacion <= 5):
                    raise ValueError("La calificación debe estar entre 1 y 5.")
                plataforma.completar_sesion(id_sesion, calificacion)
            except ValueError as e:
                print(f"Error: {e}. Ingrese un número entero válido entre 1 y 5.")
        
        elif opcion == "12": # Mostrar Historial General
            plataforma.mostrar_historial_general_sesiones()

        elif opcion == "13": # Salir
            print("Saliendo de TutorIAConnectPro. ¡Guardando datos y hasta luego!")
            plataforma._guardar_datos() # Asegurar que se guarden los datos al salir
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo con una opción del menú.")

if __name__ == "__main__":
    main()