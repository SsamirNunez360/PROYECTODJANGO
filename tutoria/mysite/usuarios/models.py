from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class MiUserManager(BaseUserManager):
    """Manager personalizado para la autenticación por correo."""
    def get_by_natural_key(self, correo):
        return self.get(correo=correo)

    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo debe ser proporcionado.')
            
        correo = self.normalize_email(correo)
        
        # Valores predeterminados para campos de la BD (asumiendo '0' como False)
        extra_fields.setdefault('is_staff_db', '0')
        extra_fields.setdefault('is_superuser_db', '0')
        extra_fields.setdefault('is_active_db', '1')
        # Puedes añadir valores iniciales para 'date_joined_db' si lo necesitas

        # Crea el usuario usando los campos de la BD
        user = self.model(correo=correo, **extra_fields)
        
        if password:
            user.set_password(password) # Usa set_password para hashear
            
        user.save(using=self._db)
        return user
        
    def create_superuser(self, correo, password=None, **extra_fields):
        # Aseguramos que los campos de la BD se establezcan como True ('1')
        extra_fields.setdefault('is_staff_db', '1')
        extra_fields.setdefault('is_superuser_db', '1')
        extra_fields.setdefault('is_active_db', '1')
        
        if extra_fields.get('is_staff_db') not in ('1', 'True'):
            raise ValueError('Superuser debe tener is_staff_db=1.')
        if extra_fields.get('is_superuser_db') not in ('1', 'True'):
            raise ValueError('Superuser debe tener is_superuser_db=1.')
            
        # Creamos el usuario, el cual usará los extra_fields para los campos _db
        return self.create_user(correo, password, **extra_fields)


class UsuarioPersonalizado(AbstractBaseUser, PermissionsMixin):
    # Campos mapeados EXACTAMENTE a tu tabla tbl_Usuarios
    idUsuario = models.AutoField(primary_key=True, db_column='idUsuario')
    correo = models.EmailField(unique=True, db_column='correo', max_length=100)
    password = models.CharField(max_length=128, db_column='password') # Se usará para almacenar el hash
    nombre = models.CharField(max_length=100, db_column='nombre')
    apellido = models.CharField(max_length=100, db_column='apellido')
    tipo = models.CharField(max_length=100, db_column='tipo')
    
    # Campos de Django mapeados a VARCHAR/CHAR de la BD con el sufijo '_db'
    last_login_db = models.CharField(max_length=100, db_column='last_login', null=True, blank=True)
    is_superuser_db = models.CharField(max_length=100, db_column='is_superuser', default='0')
    is_staff_db = models.CharField(max_length=100, db_column='is_staff', default='0')
    is_active_db = models.CharField(max_length=100, db_column='is_active', default='1')
    date_joined_db = models.CharField(max_length=100, db_column='date_joined', default=timezone.now) 
    
    # ----------------------------------------------------
    # Configuración de autenticación
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'tipo']
    
    objects = MiUserManager()

    class Meta:
        db_table = 'tbl_Usuarios'
        managed = False  # MUY IMPORTANTE: Indica que la tabla ya existe
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

    # ----------------------------------------------------
    # Mapeo de Propiedades: Convierte los CharField de la BD a Booleanos para Django
    # ----------------------------------------------------
    @property
    def is_staff(self):
        """Requerido por PermissionsMixin. Lee el campo de la BD."""
        return self.is_staff_db in ('1', 'True')

    @property
    def is_active(self):
        """Requerido por AbstractBaseUser. Lee el campo de la BD."""
        return self.is_active_db in ('1', 'True')
        
    @property
    def is_superuser(self):
        """Requerido por PermissionsMixin. Lee el campo de la BD."""
        return self.is_superuser_db in ('1', 'True')
        
    # ----------------------------------------------------
    # Lógica de Migración de Contraseña
    # ----------------------------------------------------
    def check_password(self, raw_password):
        """
        Verifica la contraseña. Si no está hasheada, usa el texto plano 
        de la BD y la migra automáticamente.
        """
        # 1. Intenta la verificación estándar de Django (para contraseñas hasheadas)
        verification_passed = super().check_password(raw_password)

        if verification_passed:
            return True
        
        # 2. Si falla el hash, verifica si coincide con el texto plano almacenado
        #    Esto solo debería ocurrir antes de la primera autenticación post-migración
        if raw_password == self.password:
            print(f"⚠️ Migrando contraseña a hash para usuario: {self.correo}...")
            # 3. Migrar: Hashea la contraseña y la guarda
            self.set_password(raw_password)
            self.save(update_fields=['password']) # Solo actualiza la columna password
            return True
            
        return False

    # ----------------------------------------------------
    # Métodos de Permisos
    # ----------------------------------------------------
    # Estos ahora usan las propiedades @is_staff/@is_superuser
    def has_perm(self, perm, obj=None):
        return self.is_superuser # Un superusuario tiene todos los permisos

    def has_module_perms(self, app_label):
        return self.is_superuser