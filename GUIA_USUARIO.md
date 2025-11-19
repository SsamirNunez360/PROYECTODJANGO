# 🎯 GUÍA DE USO - LOGIN CON MARIADB

## ✅ Estado Actual

Tu proyecto **está completamente configurado y funcionando** con MariaDB.

**Base de datos:** `db_Tutoria`  
**Tabla:** `tbl_Usuarios`  
**Estado:** ✅ LISTO PARA USAR

---

## 🚀 Iniciar la Aplicación

### Opción 1: Usar el script de inicio (Recomendado)
```bash
bash /var/www/html/PROYECTODJANGO/iniciar_servidor.sh
```

### Opción 2: Comando manual
```bash
cd /var/www/html/PROYECTODJANGO/tutoria/mysite
/var/www/html/PROYECTODJANGO/venv/bin/python manage.py runserver
```

### Opción 3: Iniciar en puerto específico
```bash
cd /var/www/html/PROYECTODJANGO/tutoria/mysite
/var/www/html/PROYECTODJANGO/venv/bin/python manage.py runserver 0.0.0.0:8080
```

---

## 🔐 Acceder a la Aplicación

Una vez que el servidor esté corriendo:

1. **Abre tu navegador** y ve a:
   ```
   http://localhost:8000
   ```

2. **Haz clic en "Iniciar Sesión"** o ve directamente a:
   ```
   http://localhost:8000/login/
   ```

3. **Ingresa tus credenciales:**

   | Email | Contraseña |
   |-------|-----------|
   | admin@outlook.com | admin123 |
   | ssamirnunez@outlook.com | admin123 |
   | almabetancourth@outlook.com | admin123 |
   | gabrielareyes@outlook.com | admin123 |
   | wilmernunez@outlook.com | admin123 |

4. **Haz clic en "Enviar"**

---

## 🧪 Verificar que Todo Funciona

### Probar la autenticación
```bash
cd /var/www/html/PROYECTODJANGO/tutoria/mysite
/var/www/html/PROYECTODJANGO/venv/bin/python /var/www/html/PROYECTODJANGO/test_login_completo.py
```

### Ver datos directos de la BD
```bash
/var/www/html/PROYECTODJANGO/venv/bin/python /var/www/html/PROYECTODJANGO/check_db_direct.py
```

---

## 📊 Información de Conexión

```
HOST:       localhost
USUARIO:    admin
CONTRASEÑA: 123
BD:         db_Tutoria
TABLA:      tbl_Usuarios
```

---

## 🆘 Solución de Problemas

### 1. Error: "Credenciales incorrectas"
- ✓ Verifica el **email exacto** (sensible a mayúsculas)
- ✓ Verifica la **contraseña exacta** (siempre es: `admin123`)
- ✓ Ejecuta: `python check_db_direct.py` para verificar

### 2. Error: "No se puede conectar a la BD"
- ✓ Verifica que MariaDB esté corriendo
- ✓ Verifica credenciales en `settings.py`
- ✓ Verifica que la BD `db_Tutoria` existe

### 3. Error: "Tabla no encontrada"
- ✓ Ejecuta: `python manage.py migrate`
- ✓ Verifica que la tabla `tbl_Usuarios` existe en DBDever

### 4. "¡El puerto 8000 ya está en uso!"
Usa otro puerto:
```bash
python manage.py runserver 0.0.0.0:8080
```

---

## 📝 Cambios Realizados en el Código

### Archivo: `usuarios/models.py`
- ✅ Agregado método `check_password()` personalizado
- ✅ Detecta automáticamente contraseñas en texto plano

### Archivo: `mysite/clases.py`
- ✅ Actualizada función `iniciar_sesion()`
- ✅ Ahora usa Django ORM y BD en lugar de JSON

### Archivo: `mysite/views.py`
- ✅ Actualizada vista `iniciar()`
- ✅ Guarda datos correctamente en sesión

### Archivo: `settings.py`
- ✅ Configuración de BD ya estaba correcta

---

## 🔄 Próximos Pasos

1. **Crear nuevo usuario desde la interfaz**
   - Implementar formulario de registro
   - Hashear contraseñas automáticamente

2. **Agregar roles y permisos**
   - Diferenciar entre Estudiante y Tutor
   - Implementar panel de administración

3. **Mejorar seguridad**
   - Hashear contraseñas existentes
   - Implementar validación de email
   - Agregar restricciones de acceso

4. **Agregar funcionalidades**
   - Recuperación de contraseña
   - Cambio de contraseña
   - Perfil de usuario

---

## 📞 Soporte

Si tienes dudas o problemas:

1. Revisa el archivo `INTEGRACION_MARIADB.md`
2. Ejecuta los scripts de diagnóstico
3. Verifica los logs de Django en la terminal

---

**Última actualización:** 14 de noviembre de 2025  
**Versión:** 1.0  
**Estado:** ✅ PRODUCTIVO

¡Tu sistema de login está listo para usar! 🎉
