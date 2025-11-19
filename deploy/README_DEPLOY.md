# Despliegue en Apache para este proyecto

Este documento describe los pasos para replicar la "Fase 3" descrita: crear el VirtualHost de Apache, ajustar permisos y configurar SELinux y el firewall. Las instrucciones están orientadas a sistemas RHEL/CentOS y derivados como AlmaLinux (httpd + SELinux + firewall-cmd). Para Debian/Ubuntu algunas rutas de usuario/servicio cambian (apache -> www-data, systemctl restart apache2, y configuración en /etc/apache2/sites-available).

Resumen de acciones a realizar (orden recomendado):

1. Preparar el virtualenv y recopilar estáticos
   - Crear y activar el virtualenv en el servidor:
     source /path/to/venv/bin/activate
   - Instalar dependencias (usa requirements.txt si aplica)
   - Ejecutar collectstatic:
     python /var/www/PROYECTODJANGO/tutoria/mysite/manage.py collectstatic --noinput

2. Copiar plantilla de VirtualHost al servidor y ajustarla
   - Plantilla en el repo: `deploy/apache/proyectoSOI.conf.template`
   - Edita:
     - `ServerName` (tu dominio o IP)
     - `python-home` en `WSGIDaemonProcess` -> la ruta completa del virtualenv
     - `WSGIScriptAlias` y `Alias` si moviste el proyecto
   - Copiar a CentOS/RHEL:
     sudo cp proyectoSOI.conf /etc/httpd/conf.d/proyectoSOI.conf
   - En Debian/Ubuntu copia a `/etc/apache2/sites-available/` y habilita con `a2ensite`.

3. Permisos del servidor web
   - Asegura que apache (usuario `apache` en CentOS, `www-data` en Debian) tenga acceso:
     sudo chown -R apache:apache /var/www/PROYECTODJANGO
     sudo mkdir -p /var/www/PROYECTODJANGO/tutoria/mysite/media
     sudo chown apache:apache /var/www/PROYECTODJANGO/tutoria/mysite/media

Nota para AlmaLinux: las instrucciones anteriores aplican tal cual en AlmaLinux (usuario del servicio `apache`, servicio `httpd`, SELinux y firewall-cmd disponibles).

4. SELinux (si está habilitado)
   - Asignar contexto R/W a directorios que el servidor debe escribir:
     sudo chcon -R -t httpd_sys_rw_content_t /var/www/PROYECTODJANGO/tutoria/mysite/staticfiles
     sudo chcon -R -t httpd_sys_rw_content_t /var/www/PROYECTODJANGO/tutoria/mysite/media
     sudo chcon -R -t httpd_sys_rw_content_t /var/www/PROYECTODJANGO/tutoria/mysite/datos
     (si usas sqlite) sudo chcon -R -t httpd_sys_rw_content_t /var/www/PROYECTODJANGO/tutoria/mysite/db.sqlite3
   - Permitir a Apache conectarse por red a BD (MariaDB remota/localhost):
     sudo setsebool -P httpd_can_network_connect_db 1
   - Dar contexto de ejecución al virtualenv (permite ejecutar scripts desde apache/mod_wsgi):
     sudo chcon -R -t httpd_sys_script_exec_t /path/to/venv

Nota: el script `deploy/deploy_apache_commands.sh` detecta si SELinux está presente (comprueba `getenforce`) y aplicará los `chcon` y `setsebool` sólo cuando SELinux esté activo (Enforcing/Permissive). Aun así, revisa los logs de SELinux si algo falla.

5. Firewall y reinicio de servicios
   - Abrir puerto HTTP:
     sudo firewall-cmd --add-service=http --permanent
     sudo firewall-cmd --reload
   - Reiniciar Apache:
     sudo systemctl restart httpd
   - Opcional: reiniciar NetworkManager si cambias settings de red

6. Verificación
   - Revisar estado del servicio:
     sudo systemctl status httpd
   - Revisar logs:
     tail -n 200 /var/log/httpd/proyectoSOI_error.log
     tail -n 200 /var/log/httpd/proyectoSOI_access.log
   - Verificar SELinux:
     getenforce
     sudo sealert -a /var/log/audit/audit.log

Archivos añadidos en este repo
- `deploy/apache/proyectoSOI.conf.template` — plantilla de VirtualHost adaptada al proyecto.
- `deploy/deploy_apache_commands.sh` — script con los comandos (para revisar y ejecutar con sudo en el servidor).
- `deploy/README_DEPLOY.md` — esta guía.

Antes de ejecutar el script, dale permisos de ejecución y revísalo:

```bash
chmod +x deploy/deploy_apache_commands.sh
# Edita deploy/deploy_apache_commands.sh y fija PROJECT_ROOT y VENV
sudo ./deploy/deploy_apache_commands.sh
```

Notas y recomendaciones finales
- Ajusta `ALLOWED_HOSTS` en `mysite/settings.py` con tu dominio/IP antes de poner DEBUG=False.
- Considera usar HTTPS (certbot/Let's Encrypt) y ajustar la configuración del VirtualHost para redirigir a 443.
- Si SELinux te sigue bloqueando, revisa `audit.log` y usa `audit2why`/`audit2allow` para depurar.
