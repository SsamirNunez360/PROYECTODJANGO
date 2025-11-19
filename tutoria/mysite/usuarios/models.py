from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone # Importamos timezone para la buena práctica
from django.contrib.auth.hashers import make_password, check_password

# --- 1. MANAGER PERSONALIZADO (MiUserManager) ---
class MiUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Asegura que los campos de staff y superusuario sean True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)

# --- 2. MODELO DE USUARIO (UsuarioPersonalizado) ---
class UsuarioPersonalizado(AbstractBaseUser, PermissionsMixin):
    # Campos base:
    idUsuario = models.AutoField(primary_key=True, db_column='idUsuario')
    email = models.EmailField(unique=True, db_column='correo')
    password = models.CharField(max_length=100, db_column='contrasenia')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    
    # Campos de Django para el sistema de autenticación:
    last_login = models.DateTimeField(blank=True, null=True) # 🔑 COLUMNA FALTANTE
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Configuración de Django:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'tipo']
    
    objects = MiUserManager()
    
    class Meta:
        db_table = 'tbl_Usuarios' # Mapeo a tu tabla existente
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

    # Métodos de permisos (requeridos por PermissionsMixin):
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def get_group_permissions(self, obj=None):
        return set() 
        
    def get_all_permissions(self, obj=None):
        return set()
    
    def check_password(self, raw_password):
        """
        Método mejorado que verifica tanto contraseñas hasheadas como en texto plano.
        Esto es necesario porque tu BD tiene contraseñas en texto plano.
        """
        # Primero verificar si está hasheada (comienza con 'pbkdf2_', 'bcrypt$', etc.)
        if self.password.startswith(('pbkdf2_', 'bcrypt$', 'argon2')):
            # Es hasheada, usar el método de Django
            return super().check_password(raw_password)
        else:
            # Es texto plano, comparar directamente
            return raw_password == self.password