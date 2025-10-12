from django.core.management.base import BaseCommand
from services.models import Category, Service, ServiceRequest

class Command(BaseCommand):
    help = "Elimina servicios, categorías y solicitudes, dejando los usuarios intactos."

    def handle(self, *args, **options):
        ServiceRequest.objects.all().delete()
        Service.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Datos eliminados (servicios, categorías y solicitudes)."))
        self.stdout.write(self.style.WARNING("Usuarios no fueron modificados."))