from datetime import datetime
from plataforma import PlataformaTutorias

def mostrar_menu():
    print("\n== BIENVENIDO A TutorIAConnectPro ==")
    print("Seleccione una opción:")
    print("1. Registrar estudiante")
    print("2. Registrar tutor")
    print("3. Enviar solicitud de tutoría")
    print("4. Asignar siguiente tutoría")
    print("5. Ver perfil de usuario")
    print("6. Volver al perfil anterior")
    print("7. Completar sesión")
    print("8. Salir")

def main():
    plataforma = PlataformaTutorias()

    while True:
        mostrar_menu()
        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre del estudiante: ")
            email = input("Email: ")
            nivel = input("Nivel académico: ")
            materias = input("Materias de interés (separadas por coma): ").split(",")
            id_est = plataforma.registrar_estudiante(nombre, email, nivel, [m.strip() for m in materias])
            print(f"Estudiante registrado con ID: {id_est}")

        elif opcion == "2":
            nombre = input("Nombre del tutor: ")
            email = input("Email: ")
            especialidad = input("Materias de especialidad (separadas por coma): ").split(",")
            calificacion = float(input("Calificación promedio: "))
            disponibilidad = {}
            print("Ingrese horarios disponibles (formato: YYYY-MM-DD HH:MM), escriba 'fin' para terminar:")
            while True:
                entrada = input("Hora disponible: ")
                if entrada.lower() == "fin":
                    break
                disponibilidad[entrada] = "libre"
            id_tutor = plataforma.registrar_tutor(nombre, email, [m.strip() for m in especialidad], calificacion, disponibilidad)
            print(f"Tutor registrado con ID: {id_tutor}")

        elif opcion == "3":
            id_est = input("ID del estudiante: ")
            materia = input("Materia para tutoría: ")
            plataforma.solicitar_tutoria(id_est, materia)
            print("Solicitud enviada.")

        elif opcion == "4":
            plataforma.asignar_tutoria_a_solicitud()

        elif opcion == "5":
            id_usuario = input("ID de usuario: ")
            plataforma.mostrar_perfil_usuario(id_usuario)

        elif opcion == "6":
            plataforma.volver_perfil_anterior()

        elif opcion == "7":
            id_sesion = input("ID de sesión: ")
            calificacion = int(input("Calificación dada al tutor (1 a 5): "))
            plataforma.completar_sesion(id_sesion, calificacion)

        elif opcion == "8":
            print("Gracias por usar TutorIAConnectPro. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
