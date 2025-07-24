from clases import TutorIAConnectPro


def ejecutar_app():
    app = TutorIAConnectPro()
    app.cargar_datos()

    while True:
        print("\n== BIENVENIDO A TutorIAConnectPro ==")
        print("Seleccione una opción:")
        print("1. Registrar estudiante")
        print("2. Registrar tutor")
        print("3. Enviar solicitud de tutoría")
        print("4. Procesar siguiente solicitud")
        print("5. Ver historial de estudiante")
        print("6. Ver historial de tutor")
        print("7. Mostrar tutores por calificación")
        print("8. Ver prerrequisitos de una materia")
        print("9. Salir")

        opcion = input("\nIngrese una opción: ")

        if opcion == '1':
            id_est = input("ID del estudiante: ")
            nombre = input("Nombre: ")
            carrera = input("Carrera: ")
            app.registrar_estudiante(id_est, nombre, carrera)

        elif opcion == '2':
            id_tutor = input("ID del tutor: ")
            nombre = input("Nombre: ")
            materias = input("Materias que imparte (separadas por coma): ").split(',')
            materias = [m.strip() for m in materias]
            calificaciones = {}
            for materia in materias:
                calificacion = float(input(f"Calificación en {materia}: "))
                calificaciones[materia] = calificacion
            app.registrar_tutor(id_tutor, nombre, materias, calificaciones)

        elif opcion == '3':
            id_est = input("ID del estudiante: ")
            materia = input("Materia para tutoría: ")
            app.enviar_solicitud(id_est, materia)

        elif opcion == '4':
            app.procesar_siguiente_solicitud()

        elif opcion == '5':
            id_est = input("ID del estudiante: ")
            app.ver_historial_estudiante(id_est)

        elif opcion == '6':
            id_tutor = input("ID del tutor: ")
            app.ver_historial_tutor(id_tutor)

        elif opcion == '7':
            app.mostrar_tutores_por_calificacion()

        elif opcion == '8':
            materia = input("Ingrese la materia: ")
            app.ver_prerrequisitos(materia)

        elif opcion == '9':
            print("Guardando datos y saliendo...")
            app.guardar_datos()
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar_app()
