from django.core.management.base import BaseCommand
import json
from usuarios.models import UsuarioPersonalizado

class Command(BaseCommand):
    help = 'Carga usuarios desde usuarios.json'

    def handle(self, *args, **kwargs):
        with open('mysite/data/usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)

        for u in usuarios:
            if not UsuarioPersonalizado.objects.filter(email=u['email']).exists():
                UsuarioPersonalizado.objects.create_user(
                    email=u['email'],
                    password=u['password'],
                    nombre=u['nombre'],
                    apellido=u['apellido'],
                    tipo=u['tipo'],
                )
                self.stdout.write(self.style.SUCCESS(f"Usuario {u['email']} creado"))
            else:
                self.stdout.write(f"Usuario {u['email']} ya existe")
