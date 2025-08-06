# auth.py
class AuthService:
    def __init__(self, plataforma):
        self.plataforma = plataforma

    def iniciar_sesion(self, email, password):
        """
        Verifica si el email y password coinciden con un estudiante o tutor.
        Retorna el usuario si es correcto, o None si falla.
        """

        # Buscar en estudiantes
        for estudiante in self.plataforma.diccionario_estudiantes.values():
            if estudiante.email == email and estudiante.password == password:
                return estudiante
        
        # Buscar en tutores
        for tutor in self.plataforma.diccionario_tutores.values():
            if tutor.email == email and tutor.password == password:
                return tutor
        
        # Si no se encontró usuario o contraseña incorrecta
        return None
