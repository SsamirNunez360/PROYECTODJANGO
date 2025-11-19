# 📋 RESUMEN DE INTEGRACIÓN CON MARIADB

## ✅ Cambios Realizados

Tu proyecto Django ahora está **completamente integrado con MariaDB** en la base de datos `db_Tutoria`, tabla `tbl_Usuarios`.

### 1. **Instalación de Dependencias**
- ✓ `mysqlclient` - Driver para conectar con MariaDB
- ✓ `PyMySQL` - Alternativa de PyMySQL
- Actualizado `requirements.txt`

### 2. **Configuración de Base de Datos**
- ✓ `settings.py` ya estaba configurado correctamente con:
  - `ENGINE: 'django.db.backends.mysql'`
  - Base de datos: `db_Tutoria`
  - Usuario: `admin`
  - Contraseña: `123`

### 3. **Modelo de Usuario Actualizado**
**Archivo:** `/tutoria/mysite/usuarios/models.py`

Cambios principales:
- Agregado método `check_password()` personalizado que:
  - Reconoce contraseñas en texto plano (tu BD actual)
  - Reconoce contraseñas hasheadas (para compatibilidad futura)
  - Compara automáticamente según el formato

### 4. **Función de Login Actualizada**
**Archivo:** `/tutoria/mysite/mysite/clases.py`

La función `PlataformaTutorias.iniciar_sesion()` ahora:
- Busca usuarios en la BD usando Django ORM
- Verifica contraseñas automáticamente
- Retorna un objeto `ResultadoLogin` con los datos del usuario
- Maneja excepciones correctamente

### 5. **Vista de Login Actualizada**
**Archivo:** `/tutoria/mysite/mysite/views.py`

La función `iniciar(request)` ahora:
- Guarda datos correctos de usuario en la sesión
- Usa el campo `idUsuario` de la BD
- Redirige según el tipo de usuario

---

## 🔐 Credenciales de Prueba

Usuarios disponibles en tu base de datos:

| Email | Contraseña | Nombre | Tipo |
|-------|-----------|--------|------|
| admin@outlook.com | admin123 | Fix | administrador |
| ssamirnunez@outlook.com | admin123 | Samir Nunez | administrador |
| almabetancourth@outlook.com | admin123 | Alma Betancourth | administrador |
| gabrielareyes@outlook.com | admin123 | Gabriela Reyes | administrador |
| wilmernunez@outlook.com | admin123 | Wilmer Nuñez | administrador |

---

## 🚀 Cómo Usar

### Iniciar Sesión
1. Ve a `http://localhost:8000/login/`
2. Ingresa un email de la tabla anterior
3. Contraseña: `admin123`
4. Haz clic en "Iniciar Sesión"

### Ejecutar el Servidor
```bash
cd /var/www/html/PROYECTODJANGO/tutoria/mysite
/var/www/html/PROYECTODJANGO/venv/bin/python manage.py runserver
```

### Pruebas de Autenticación
```bash
# Probar modelo y autenticación
/var/www/html/PROYECTODJANGO/venv/bin/python test_auth.py

# Probar flujo completo de login
/var/www/html/PROYECTODJANGO/venv/bin/python test_login_completo.py

# Verificar datos directamente
/var/www/html/PROYECTODJANGO/venv/bin/python check_db_direct.py
```

---

## 📝 Notas Importantes

### Sobre las Contraseñas
Tu base de datos tiene contraseñas en **texto plano**. Para mayor seguridad, deberías:

1. **Opción A: Hashear las contraseñas existentes**
```bash
cd /var/www/html/PROYECTODJANGO/tutoria/mysite
python manage.py shell
```

```python
from usuarios.models import UsuarioPersonalizado
for user in UsuarioPersonalizado.objects.all():
    user.set_password('admin123')  # Hashea la contraseña
    user.save()
```

2. **Opción B: Usar la solución actual** (funciona, pero menos segura)
   - Requiere que contraseñas estén en texto plano
   - El modelo lo detecta automáticamente

### Estructura de la Tabla
```
tbl_Usuarios:
- idUsuario (INT PRIMARY KEY)
- correo (VARCHAR - EMAIL)
- contrasenia (VARCHAR - TEXTO PLANO O HASHEADO)
- nombre (VARCHAR)
- apellido (VARCHAR)
- tipo (VARCHAR)
- last_login (DATETIME)
- is_active (TINYINT)
- is_staff (TINYINT)
- is_superuser (TINYINT)
```

---

## ✨ Próximos Pasos Sugeridos

1. **Validar tipos de usuario** - Ajustar según tus necesidades (estudiante/tutor)
2. **Registrar nuevos usuarios** - Crear comando para agregar desde formulario
3. **Hashear contraseñas existentes** - Por seguridad
4. **Implementar recuperación de contraseña** - Functionality adicional
5. **Agregar logs de acceso** - Para auditoría

---

## 🐛 Solución de Problemas

### ¿Sigue diciendo "credenciales incorrectas"?

1. Verifica el email exacto en DBDever
2. Verifica la contraseña exacta (sensible a mayúsculas)
3. Ejecuta el script de diagnóstico:
   ```bash
   python check_db_direct.py
   ```

### ¿Conexión a BD rechazada?

Verifica en `settings.py`:
- Host correcto: `localhost`
- Usuario correcto: `admin`
- Contraseña correcta: `123`
- BD correcta: `db_Tutoria`

---

**Última actualización:** 14 de noviembre de 2025
**Estado:** ✅ Login con MariaDB Funcionando
