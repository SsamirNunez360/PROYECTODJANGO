"""
Comando Django para cargar usuarios desde archivos JSON a la base de datos MariaDB.

Uso:
    python manage.py cargar_usuarios_desde_json
"""

import json
import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from usuarios.models import UsuarioPersonalizado
from django.conf import settings


class Command(BaseCommand):
    help = 'Carga usuarios desde archivos JSON a la base de datos MariaDB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--archivo',
            type=str,
            help='Ruta específica al archivo JSON a cargar (opcional)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los usuarios existentes antes de cargar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            confirm = input("¿Estás seguro de que deseas eliminar TODOS los usuarios? (s/n): ")
            if confirm.lower() == 's':
                UsuarioPersonalizado.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('✓ Todos los usuarios han sido eliminados.'))
            else:
                self.stdout.write(self.style.WARNING('Operación cancelada.'))
                return

        archivo_especifico = options.get('archivo')
        
        if archivo_especifico:
            # Cargar un archivo específico
            self.cargar_archivo_json(archivo_especifico)
        else:
            # Cargar archivos por defecto
            base_dir = Path(settings.BASE_DIR)
            data_dir = base_dir / 'mysite' / 'data'
            
            archivos = {
                'estudiantes.json': 'Estudiante',
                'tutores.json': 'Tutor',
            }
            
            for nombre_archivo, tipo_usuario in archivos.items():
                ruta = data_dir / nombre_archivo
                if ruta.exists():
                    self.cargar_archivo_json(str(ruta), tipo_usuario)
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ No se encontró: {ruta}')
                    )

    def cargar_archivo_json(self, ruta_archivo, tipo_usuario=None):
        """Carga usuarios desde un archivo JSON específico."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                usuarios_data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'El archivo {ruta_archivo} no existe.')
        except json.JSONDecodeError as e:
            raise CommandError(f'Error al decodificar JSON en {ruta_archivo}: {e}')

        if not isinstance(usuarios_data, list):
            raise CommandError(f'El archivo {ruta_archivo} debe contener una lista de usuarios.')

        usuarios_creados = 0
        usuarios_actualizados = 0
        errores = 0

        for usuario_dict in usuarios_data:
            try:
                email = usuario_dict.get('email') or usuario_dict.get('correo')
                nombre = usuario_dict.get('nombre', 'Desconocido')
                apellido = usuario_dict.get('apellido', '')
                password = usuario_dict.get('password') or usuario_dict.get('contrasenia', '12345678')
                tipo = tipo_usuario or usuario_dict.get('tipo', 'Estudiante')

                if not email:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Usuario sin email ignorado: {nombre}')
                    )
                    continue

                # Intentar obtener o crear el usuario
                usuario, created = UsuarioPersonalizado.objects.get_or_create(
                    email=email,
                    defaults={
                        'nombre': nombre,
                        'apellido': apellido,
                        'tipo': tipo,
                        'is_active': True,
                    }
                )

                # Actualizar o establecer la contraseña
                if created or not usuario.password:
                    usuario.set_password(password)
                    usuario.save()
                    usuarios_creados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Creado: {nombre} ({email})')
                    )
                else:
                    usuarios_actualizados += 1
                    self.stdout.write(
                        self.style.WARNING(f'→ Existía: {nombre} ({email})')
                    )

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Error cargando {usuario_dict.get("email")}: {e}')
                )

        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✓ Creados: {usuarios_creados}'))
        self.stdout.write(self.style.WARNING(f'→ Actualizados: {usuarios_actualizados}'))
        if errores > 0:
            self.stdout.write(self.style.ERROR(f'✗ Errores: {errores}'))
        self.stdout.write('='*50)
