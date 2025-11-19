#!/bin/bash

# Script para iniciar el servidor Django

echo "================================"
echo "🚀 INICIANDO SERVIDOR DJANGO"
echo "================================"
echo ""
echo "Base de datos: db_Tutoria (MariaDB)"
echo "Credenciales: admin / 123"
echo ""
echo "Usuarios disponibles:"
echo "  - admin@outlook.com (admin123)"
echo "  - ssamirnunez@outlook.com (admin123)"
echo "  - almabetancourth@outlook.com (admin123)"
echo "  - gabrielareyes@outlook.com (admin123)"
echo "  - wilmernunez@outlook.com (admin123)"
echo ""
echo "URL de la aplicación: http://localhost:8000"
echo "URL de login: http://localhost:8000/login/"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "================================"
echo ""

cd /var/www/html/PROYECTODJANGO/tutoria/mysite
/var/www/html/PROYECTODJANGO/venv/bin/python manage.py runserver 0.0.0.0:8000
