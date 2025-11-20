from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
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

        # Crea el usuario usando los campos de la BD
        user = self.model(correo=correo, **extra_fields)
        
        if password:
            user.password = make_password(password)  # Hashear contraseña
            
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


class UsuarioPersonalizado(models.Model):
    # Campos mapeados EXACTAMENTE a tu tabla tbl_Usuarios
    idUsuario = models.AutoField(primary_key=True, db_column='idUsuario')
    correo = models.EmailField(unique=True, db_column='correo', max_length=100)
    password = models.CharField(max_length=128, db_column='password')
    nombre = models.CharField(max_length=100, db_column='nombre')
    apellido = models.CharField(max_length=100, db_column='apellido')
    tipo = models.CharField(max_length=100, db_column='tipo')
    is_superuser = models.CharField(max_length=100, db_column='is_superuser', default='0')
    is_staff = models.CharField(max_length=100, db_column='is_staff', default='0')
    is_active = models.CharField(max_length=100, db_column='is_active', default='1')
    last_login = models.CharField(max_length=100, db_column='last_login', null=True, blank=True)
    date_joined = models.DateTimeField(db_column='date_joined', null=True, blank=True) 
    
    # --- Configuración de autenticación (NO usamos AbstractBaseUser para evitar conflictos)
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'tipo']
    
    objects = MiUserManager()

    class Meta:
        db_table = 'tbl_Usuarios'
        managed = False
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

    # ----------------------------------------------------
    # Mapeo de Propiedades: Convierte los CharField de la BD a Booleanos para Django
    # ----------------------------------------------------
    @property
    def is_staff_bool(self):
        """Convierte el campo is_staff a booleano."""
        return self.is_staff in ('1', 'True')

    @property
    def is_active_bool(self):
        """Convierte el campo is_active a booleano."""
        return self.is_active in ('1', 'True')
        
    @property
    def is_superuser_bool(self):
        """Convierte el campo is_superuser a booleano."""
        return self.is_superuser in ('1', 'True')
        
    # ----------------------------------------------------
    # Lógica de Verificación de Contraseña
    # ----------------------------------------------------
    def check_password(self, raw_password):
        """
        Verifica la contraseña usando el sistema de hashing de Django.
        """
        return check_password(raw_password, self.password)
    
    def set_password(self, raw_password):
        """
        Hashea y guarda la contraseña.
        """
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    # ----------------------------------------------------
    # Métodos de Permisos
    # ----------------------------------------------------
    def has_perm(self, perm, obj=None):
        return self.is_superuser # Un superusuario tiene todos los permisos

    def has_module_perms(self, app_label):
        return self.is_superuser