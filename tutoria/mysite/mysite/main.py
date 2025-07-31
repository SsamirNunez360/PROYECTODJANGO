from clases import PlataformaTutorias
from datetime import datetime

def mostrar_menu():
    """Muestra las opciones del menú principal."""
    print("\n== BIENVENIDO A TutorIAConnectpro ==")
    print("\n--- GESTIÓN DE USUARIOS (CRUD) ---")
    print("1. Registrar nuevo Estudiante")
    print("2. Registrar nuevo Tutor")
    print("3. Ver perfil de Usuario (Estudiante/Tutor)")
    print("4. Listar todos los Estudiantes")
    print("5. Listar todos los Tutores")
    print("6. Actualizar información de Usuario (Estudiante/Tutor)")
    print("7. Eliminar Usuario (Estudiante/Tutor)")
    print("\n--- GESTIÓN DE TUTORÍAS ---")
    print("8. Enviar solicitud de tutoría")
    print("9. Listar solicitudes pendientes")
    print("10. Asignar siguiente tutoría")
    print("11. Completar sesión de tutoría y calificar")
    print("12. Mostrar historial general de sesiones")
    print("\n13. Salir")
    print("====================================")

def main():
    """Función principal para ejecutar la aplicación."""
    plataforma = PlataformaTutorias()

    while True:
        mostrar_menu()
        opcion = input("Ingrese su opción: ")

        if opcion == '1':
            print("\n--- REGISTRAR NUEVO ESTUDIANTE ---")
            nombre = input("Nombre del estudiante: ")
            email = input("Email del estudiante: ")
            nivel = input("Nivel académico (Ej: Universitario, Bachillerato): ")
            materias_interes_str = input("Materias de interés (separadas por coma): ")
            materias_interes = [m.strip() for m in materias_interes_str.split(',')]
            plataforma.registrar_estudiante(nombre, email, nivel, materias_interes)
        
        elif opcion == '2':
            print("\n--- REGISTRAR NUEVO TUTOR ---")
            nombre = input("Nombre del tutor: ")
            email = input("Email del tutor: ")
            especialidad_str = input("Materias de especialidad (separadas por coma): ")
            especialidad = [m.strip() for m in especialidad_str.split(',')]
            while True:
                try:
                    calificacion = float(input("Calificación promedio inicial (1.0-5.0): "))
                    if 1.0 <= calificacion <= 5.0:
                        break
                    else:
                        print("La calificación debe estar entre 1.0 y 5.0.")
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un número.")
            
            print("Ingrese la disponibilidad del tutor (YYYY-MM-DD HH:MM). Se asumirá 'libre'.")
            print("Escriba 'fin' para terminar de añadir disponibilidad.")
            disponibilidad = {}
            while True:
                entrada = input("Fecha y Hora: ")
                if entrada.lower() == 'fin':
                    break
                try:
                    datetime.strptime(entrada, "%Y-%m-%d %H:%M") # Validar formato
                    disponibilidad[entrada] = 'libre' # Asignar automáticamente como 'libre'
                except ValueError:
                    print("Formato incorrecto. Use 'YYYY-MM-DD HH:MM'.")
                except Exception as e:
                    print(f"Error inesperado al procesar disponibilidad: {e}")

            plataforma.registrar_tutor(nombre, email, especialidad, calificacion, disponibilidad)

        elif opcion == '3':
            print("\n--- VER PERFIL DE USUARIO ---")
            id_usuario = input("Ingrese el ID del usuario (Ej: E001, T001): ").upper()
            plataforma.mostrar_perfil_usuario(id_usuario)

        elif opcion == '4':
            plataforma.listar_estudiantes()

        elif opcion == '5':
            plataforma.listar_tutores()
            
        elif opcion == '6':
            print("\n--- ACTUALIZAR INFORMACIÓN DE USUARIO ---")
            id_usuario = input("Ingrese el ID del usuario a actualizar (Ej: E001, T001): ").upper()
            
            # Determinar automáticamente el tipo de usuario
            if id_usuario.startswith('E'):
                tipo_usuario_detectado = 'Estudiante'
            elif id_usuario.startswith('T'):
                tipo_usuario_detectado = 'Tutor'
            else:
                print("ID de usuario inválido. El ID debe comenzar con 'E' para Estudiante o 'T' para Tutor.")
                continue

            if tipo_usuario_detectado == 'Estudiante':
                estudiante = plataforma.diccionario_estudiantes.get(id_usuario)
                if not estudiante:
                    print("Estudiante no encontrado.")
                    continue
                
                print(f"Actualizando estudiante: {estudiante.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (actual: {estudiante.nombre}, dejar vacío para no cambiar): ")
                nuevo_email = input(f"Nuevo email (actual: {estudiante.email}, dejar vacío para no cambiar): ")
                nuevo_nivel = input(f"Nuevo nivel académico (actual: {estudiante.nivel_academico}, dejar vacío para no cambiar): ")
                nuevas_materias_str = input(f"Nuevas materias de interés (actual: {', '.join(estudiante.materias_interes)}, dejar vacío para no cambiar, separar por coma): ")

                plataforma.actualizar_estudiante(
                    id_usuario,
                    nuevo_nombre if nuevo_nombre else None,
                    nuevo_email if nuevo_email else None,
                    nuevo_nivel if nuevo_nivel else None,
                    [m.strip() for m in nuevas_materias_str.split(',')] if nuevas_materias_str else None
                )
            elif tipo_usuario_detectado == 'Tutor':
                tutor = plataforma.diccionario_tutores.get(id_usuario)
                if not tutor:
                    print("Tutor no encontrado.")
                    continue
                
                print(f"Actualizando tutor: {tutor.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (actual: {tutor.nombre}, dejar vacío para no cambiar): ")
                nuevo_email = input(f"Nuevo email (actual: {tutor.email}, dejar vacío para no cambiar): ")
                nuevas_especialidades_str = input(f"Nuevas materias de especialidad (actual: {', '.join(tutor.materias_especialidad)}, dejar vacío para no cambiar, separar por coma): ")
                
                nueva_calificacion_str = input(f"Nueva calificación promedio (actual: {tutor.calificacion_promedio:.1f}, dejar vacío para no cambiar): ")
                nueva_calificacion = float(nueva_calificacion_str) if nueva_calificacion_str else None

                print("Actualizar disponibilidad (Ingrese 'YYYY-MM-DD HH:MM' o 'fin'). Se asumirá 'libre' por defecto.")
                nueva_disponibilidad = {}
                while True:
                    entrada = input("Fecha y Hora: ")
                    if entrada.lower() == 'fin':
                        break
                    try:
                        datetime.strptime(entrada, "%Y-%m-%d %H:%M") # Validar formato
                        nueva_disponibilidad[entrada] = 'libre' # Asignar automáticamente como 'libre'
                    except ValueError:
                        print("Formato incorrecto. Use 'YYYY-MM-DD HH:MM'.")
                    except Exception as e:
                        print(f"Error inesperado al procesar disponibilidad: {e}")

                plataforma.actualizar_tutor(
                    id_usuario,
                    nuevo_nombre if nuevo_nombre else None,
                    nuevo_email if nuevo_email else None,
                    [m.strip() for m in nuevas_especialidades_str.split(',')] if nuevas_especialidades_str else None,
                    nueva_calificacion,
                    nueva_disponibilidad if nueva_disponibilidad else None
                )

        elif opcion == '7':
            print("\n--- ELIMINAR USUARIO ---")
            id_usuario = input("Ingrese el ID del usuario a eliminar (Ej: E001, T001): ").upper()
            
            # Determinar automáticamente el tipo de usuario
            if id_usuario.startswith('E'):
                plataforma.eliminar_estudiante(id_usuario)
            elif id_usuario.startswith('T'):
                plataforma.eliminar_tutor(id_usuario)
            else:
                print("ID de usuario inválido. El ID debe comenzar con 'E' para Estudiante o 'T' para Tutor.")

        elif opcion == '8':
            print("\n--- ENVIAR SOLICITUD DE TUTORÍA ---")
            # CAMBIO AQUÍ: Mensaje más específico para el ID
            id_estudiante = input("Ingrese el ID del estudiante solicitante (Ejemplo: E001): ").upper() 
            materia = input("Materia de la tutoría: ")
            fecha_hora_preferida = input("Fecha y hora preferida (YYYY-MM-DD HH:MM, dejar vacío si no tiene preferencia): ")
            if not fecha_hora_preferida:
                fecha_hora_preferida = None
            plataforma.solicitar_tutoria(id_estudiante, materia, fecha_hora_preferida)

        elif opcion == '9':
            plataforma.listar_solicitudes_pendientes()

        elif opcion == '10':
            plataforma.asignar_tutoria_a_solicitud()

        elif opcion == '11':
            print("\n--- COMPLETAR SESIÓN Y CALIFICAR ---")
            id_sesion = input("Ingrese el ID de la sesión a completar (Ej: S001): ").upper()
            while True:
                try:
                    calificacion = int(input("Ingrese la calificación para el tutor (1-5): "))
                    if 1 <= calificacion <= 5:
                        break
                    else:
                        print("La calificación debe ser un número entre 1 y 5.")
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un número entero.")
            plataforma.completar_sesion(id_sesion, calificacion)

        elif opcion == '12':
            plataforma.mostrar_historial_general_sesiones()

        elif opcion == '13':
            print("Gracias por usar TutorIAConnectpro. ¡Hasta luego!")
            break
        
        else:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 13.")

if __name__ == "__main__":
    main()