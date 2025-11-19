#!/usr/bin/env bash
# Script de despliegue: permisos, SELinux y firewall para CentOS/RHEL
# NO ejecutarlo sin revisar y sin sudo. Edita PROJECT_ROOT y VENV abajo.

set -euo pipefail

# --- CONFIGURA ESTAS VARIABLES ANTES DE EJECUTAR ---
PROJECT_ROOT="/var/www/PROYECTODJANGO/tutoria/mysite"
VENV="/path/to/venv"
APACHE_USER="apache" # en CentOS/RedHat. En Debian/Ubuntu usar www-data

echo "Usando PROJECT_ROOT=${PROJECT_ROOT}"
echo "Usando VENV=${VENV}"

echo "1) Crear carpeta media y asegurar permisos"
sudo mkdir -p "${PROJECT_ROOT}/media"
sudo chown -R ${APACHE_USER}:${APACHE_USER} "${PROJECT_ROOT}"
sudo chown ${APACHE_USER}:${APACHE_USER} "${PROJECT_ROOT}/media"

echo "2) collectstatic (ejecutar con tu virtualenv activo)"
echo "  Activar virtualenv y ejecutar:"
echo "    source ${VENV}/bin/activate"
echo "    python ${PROJECT_ROOT}/manage.py collectstatic --noinput"


echo "3) SELinux: establecer contextos (si SELinux está habilitado)"
if command -v getenforce >/dev/null 2>&1; then
  SELINUX_STATE=$(getenforce || true)
  echo "SELinux estado: ${SELINUX_STATE}"
  if [ "${SELINUX_STATE}" = "Enforcing" ] || [ "${SELINUX_STATE}" = "Permissive" ]; then
    echo "Aplicando contextos SELinux..."
    sudo chcon -R -t httpd_sys_rw_content_t "${PROJECT_ROOT}/staticfiles" || true
    sudo chcon -R -t httpd_sys_rw_content_t "${PROJECT_ROOT}/media" || true
    sudo chcon -R -t httpd_sys_rw_content_t "${PROJECT_ROOT}/datos" || true
    if [ -f "${PROJECT_ROOT}/db.sqlite3" ]; then
      sudo chcon -R -t httpd_sys_rw_content_t "${PROJECT_ROOT}/db.sqlite3" || true
    fi

    echo "Permitir a Apache conectarse a bases de datos por red"
    sudo setsebool -P httpd_can_network_connect_db 1 || true

    echo "Asignar contexto de ejecución al virtualenv (permite ejecutar scripts)"
    sudo chcon -R -t httpd_sys_script_exec_t "${VENV}" || true
  else
    echo "SELinux no está en modo Enforcing/Permissive — omitiendo chcon y setsebool."
  fi
else
  echo "Comando getenforce no encontrado: parece que SELinux no está instalado; omitiendo pasos SELinux."
fi

echo "4) Reiniciar servicios y abrir firewall"
if command -v firewall-cmd >/dev/null 2>&1; then
  sudo firewall-cmd --add-service=http --permanent || true
  sudo firewall-cmd --reload || true
else
  echo "firewall-cmd no disponible: asegura manualmente que el puerto 80 esté abierto si es necesario."
fi

echo "Reiniciando servicio de Apache (intentando httpd, luego apache2 si falla)"
sudo systemctl restart httpd || sudo systemctl restart apache2 || true
echo "Reiniciando NetworkManager (si aplica)"
sudo systemctl restart NetworkManager || true

echo "Hecho. Verifica los logs en /var/log/httpd/ y el estado de SELinux con: sudo getenforce && sudo sealert -a /var/log/audit/audit.log"

echo "Recuerda: revisar y adaptar ServerName y rutas en la plantilla de VirtualHost antes de copiarla a /etc/httpd/conf.d/proyectoSOI.conf"

exit 0
