import mysql.connector
from mysql.connector import Error
import hashlib
import json

class DatabaseConnection:
    """Maneja la conexión y operaciones con la base de datos MariaDB."""
    
    def __init__(self):
        self.host = "localhost"
        self.database = "db_Tutoria"
        self.user = "root"  # Cambia según tu configuración
        self.password = ""  # Cambia según tu configuración
        self.connection = None
    
    def conectar(self):
        """Establece conexión con la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
                return True
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False
    
    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")
    
    def hash_password(self, password):
        """Hashea una contraseña usando SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def iniciar_sesion(self, correo, contraseña):
        """
        Inicia sesión verificando correo y contraseña.
        Retorna un diccionario con los datos del usuario si es exitoso, None si falla.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Primero intentar con contraseña sin hashear (para las contraseñas actuales)
            query = """
                SELECT idUsuario, correo, contraseña, nombre, apellido, tipo
                FROM tbl_Usuarios 
                WHERE correo = %s AND contraseña = %s
            """
            
            cursor.execute(query, (correo, contraseña))
            usuario = cursor.fetchone()
            
            # Si no funciona, intentar con hash
            if not usuario:
                password_hash = self.hash_password(contraseña)
                cursor.execute(query, (correo, password_hash))
                usuario = cursor.fetchone()
            
            cursor.close()
            
            if usuario:
                nombre_completo = f"{usuario['nombre']} {usuario['apellido']}"
                print(f"Inicio de sesión exitoso: {nombre_completo}")
                
                # Retornar datos en formato compatible con tu sistema
                return {
                    'id_usuario': str(usuario['idUsuario']),
                    'correo': usuario['correo'],
                    'nombre': usuario['nombre'],
                    'apellido': usuario['apellido'],
                    'nombre_completo': nombre_completo,
                    'tipo_usuario': usuario['tipo']
                }
            else:
                print("Correo o contraseña incorrectos")
                return None
                
        except Error as e:
            print(f"Error al iniciar sesión: {e}")
            return None
    
    def registrar_usuario(self, nombre, apellido, correo, contraseña, tipo):
        """
        Registra un nuevo usuario en la base de datos.
        """
        try:
            cursor = self.connection.cursor()
            
            # Verificar si el correo ya existe
            cursor.execute("SELECT idUsuario FROM tbl_Usuarios WHERE correo = %s", (correo,))
            if cursor.fetchone():
                print(f"Error: El correo {correo} ya está registrado")
                cursor.close()
                return None
            
            # Hashear la contraseña (opcional, puedes dejarlo sin hash si prefieres)
            # contraseña_hash = self.hash_password(contraseña)
            
            query = """
                INSERT INTO tbl_Usuarios 
                (correo, contraseña, nombre, apellido, tipo)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            valores = (correo, contraseña, nombre, apellido, tipo)
            
            cursor.execute(query, valores)
            self.connection.commit()
            
            # Obtener el ID generado
            id_usuario = cursor.lastrowid
            cursor.close()
            
            print(f"Usuario {nombre} {apellido} registrado exitosamente con ID: {id_usuario}")
            return id_usuario
            
        except Error as e:
            print(f"Error al registrar usuario: {e}")
            self.connection.rollback()
            return None
    
    def obtener_usuario_por_id(self, id_usuario):
        """Obtiene un usuario por su ID."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT idUsuario, correo, nombre, apellido, tipo
                FROM tbl_Usuarios 
                WHERE idUsuario = %s
            """
            cursor.execute(query, (id_usuario,))
            usuario = cursor.fetchone()
            cursor.close()
            
            if usuario:
                usuario['nombre_completo'] = f"{usuario['nombre']} {usuario['apellido']}"
            
            return usuario
            
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def obtener_usuario_por_correo(self, correo):
        """Obtiene un usuario por su correo."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT idUsuario, correo, nombre, apellido, tipo
                FROM tbl_Usuarios 
                WHERE correo = %s
            """
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()
            cursor.close()
            
            if usuario:
                usuario['nombre_completo'] = f"{usuario['nombre']} {usuario['apellido']}"
            
            return usuario
            
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def actualizar_usuario(self, id_usuario, datos_actualizar):
        """Actualiza los datos de un usuario."""
        try:
            cursor = self.connection.cursor()
            
            campos = []
            valores = []
            
            if 'nombre' in datos_actualizar:
                campos.append("nombre = %s")
                valores.append(datos_actualizar['nombre'])
            
            if 'apellido' in datos_actualizar:
                campos.append("apellido = %s")
                valores.append(datos_actualizar['apellido'])
            
            if 'correo' in datos_actualizar:
                campos.append("correo = %s")
                valores.append(datos_actualizar['correo'])
            
            if 'contraseña' in datos_actualizar:
                campos.append("contraseña = %s")
                # Puedes hashear aquí si lo deseas: self.hash_password(datos_actualizar['contraseña'])
                valores.append(datos_actualizar['contraseña'])
            
            if 'tipo' in datos_actualizar:
                campos.append("tipo = %s")
                valores.append(datos_actualizar['tipo'])
            
            if not campos:
                print("No hay campos para actualizar")
                return False
            
            valores.append(id_usuario)
            query = f"UPDATE tbl_Usuarios SET {', '.join(campos)} WHERE idUsuario = %s"
            
            cursor.execute(query, valores)
            self.connection.commit()
            cursor.close()
            
            print(f"Usuario ID {id_usuario} actualizado exitosamente")
            return True
            
        except Error as e:
            print(f"Error al actualizar usuario: {e}")
            self.connection.rollback()
            return False
    
    def eliminar_usuario(self, id_usuario):
        """Elimina un usuario de la base de datos."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM tbl_Usuarios WHERE idUsuario = %s"
            cursor.execute(query, (id_usuario,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"Usuario ID {id_usuario} eliminado exitosamente")
                cursor.close()
                return True
            else:
                print(f"Usuario ID {id_usuario} no encontrado")
                cursor.close()
                return False
                
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
            self.connection.rollback()
            return False
    
    def listar_usuarios(self, tipo=None):
        """Lista todos los usuarios o filtra por tipo."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if tipo:
                query = """
                    SELECT idUsuario, correo, nombre, apellido, tipo
                    FROM tbl_Usuarios 
                    WHERE tipo = %s
                """
                cursor.execute(query, (tipo,))
            else:
                query = """
                    SELECT idUsuario, correo, nombre, apellido, tipo
                    FROM tbl_Usuarios
                """
                cursor.execute(query)
            
            usuarios = cursor.fetchall()
            cursor.close()
            
            # Agregar nombre completo
            for usuario in usuarios:
                usuario['nombre_completo'] = f"{usuario['nombre']} {usuario['apellido']}"
            
            return usuarios
            
        except Error as e:
            print(f"Error al listar usuarios: {e}")
            return []
    
    def cambiar_contraseña(self, correo, contraseña_actual, contraseña_nueva):
        """Cambia la contraseña de un usuario."""
        try:
            # Verificar contraseña actual
            usuario = self.iniciar_sesion(correo, contraseña_actual)
            if not usuario:
                print("Contraseña actual incorrecta")
                return False
            
            cursor = self.connection.cursor()
            # Puedes hashear la nueva contraseña si lo deseas
            query = "UPDATE tbl_Usuarios SET contraseña = %s WHERE correo = %s"
            cursor.execute(query, (contraseña_nueva, correo))
            self.connection.commit()
            cursor.close()
            
            print("Contraseña actualizada exitosamente")
            return True
            
        except Error as e:
            print(f"Error al cambiar contraseña: {e}")
            self.connection.rollback()
            return False