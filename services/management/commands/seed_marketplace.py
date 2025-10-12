from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Category, Service
from django.utils import timezone
from django.utils.text import slugify
import random

CATS = ["Limpieza", "Gasfitería", "Electricidad", "Lavado de autos", "Jardinería"]

class Command(BaseCommand):
    help = "Crea usuarios, categorías y servicios de prueba"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=3)
        parser.add_argument("--services", type=int, default=10)

    def handle(self, *args, **opts):
        users_n = opts["users"]
        svcs_n = opts["services"]

        # usuarios
        users = []
        for i in range(users_n):
            username = f"user{i+1}"
            user, _ = User.objects.get_or_create(username=username)
            if not user.has_usable_password():
                user.set_password("s3cret123")
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Usuarios creados: {len(users)} (pass: s3cret123)"))

        # categorías
        cats = []
        for name in CATS:
            slug = slugify(name)
            c, _ = Category.objects.get_or_create(
                slug=slug,                     # ← usamos el slug como clave de búsqueda
                defaults={"name": name},       # ← si no existe, crea con este name
            )
            cats.append(c)
        self.stdout.write(self.style.SUCCESS(f"Categorías creadas: {len(cats)}"))

        # servicios
        created = 0
        titles = [
            "Servicio de {cat}",
            "{cat} a domicilio",
            "Urgencias de {cat}",
            "Mantenimiento de {cat}"
        ]
        for _ in range(svcs_n):
            owner = random.choice(users)
            cat = random.choice(cats)
            title = random.choice(titles).format(cat=cat.name)
            svc, made = Service.objects.get_or_create(
                owner=owner,
                title=title,
                defaults={
                    "description": f"Trabajo profesional de {cat.name.lower()}",
                    "category": cat,
                    "price_from": random.randint(15000, 60000),
                    "is_active": True,
                    "created_at": timezone.now(),
                }
            )
            if made:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Servicios creados: {created}"))
        self.stdout.write(self.style.SUCCESS("Seed completado."))
