from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Service, ServiceRequest
import random

class Command(BaseCommand):
    help = "Crea solicitudes aleatorias entre los usuarios existentes."

    def add_arguments(self, parser):
        parser.add_argument("--requests", type=int, default=20)

    def handle(self, *args, **options):
        total = options["requests"]
        users = list(User.objects.filter(is_superuser=False))
        services = list(Service.objects.all())

        if not users or not services:
            self.stdout.write(self.style.ERROR("No hay usuarios o servicios para generar solicitudes."))
            return

        created = 0
        for _ in range(total):
            requester = random.choice(users)
            service = random.choice(services)
            if service.owner == requester:
                continue  # no contactarse a sí mismo
            if not ServiceRequest.objects.filter(service=service, requester=requester).exists():
                ServiceRequest.objects.create(
                    service=service,
                    requester=requester,
                    message=f"Estoy interesado en tu servicio: {service.title}",
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Solicitudes creadas: {created}"))
