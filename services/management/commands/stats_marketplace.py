from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from services.models import Category, Service, ServiceRequest


class Command(BaseCommand):
    help = "Muestra estadísticas del marketplace (usuarios, servicios, categorías y solicitudes)."

    def handle(self, *args, **options):
        total_users = User.objects.count()
        total_services = Service.objects.count()
        total_cats = Category.objects.count()
        total_requests = ServiceRequest.objects.count()

        self.stdout.write(self.style.SUCCESS("📊 ESTADÍSTICAS DEL MARKETPLACE"))
        self.stdout.write("──────────────────────────────────────────────")
        self.stdout.write(f"👤 Usuarios totales: {total_users}")
        self.stdout.write(f"🧩 Categorías totales: {total_cats}")
        self.stdout.write(f"🛠️ Servicios publicados: {total_services}")
        self.stdout.write(f"💬 Solicitudes enviadas: {total_requests}")

        # Servicios por categoría
        self.stdout.write("\n📂 Servicios por categoría:")
        for row in Category.objects.annotate(total=Count("services")).values("name", "total"):
            self.stdout.write(f"  - {row['name']}: {row['total']} servicios")

        # Servicios con solicitudes
        con_req = Service.objects.annotate(reqs=Count("requests")).filter(reqs__gt=0)
        self.stdout.write(f"\n📨 Servicios que recibieron solicitudes: {con_req.count()}")

        # Promedio de solicitudes por servicio
        if total_services > 0:
            avg_reqs = total_requests / total_services
            self.stdout.write(f"📈 Promedio de solicitudes por servicio: {avg_reqs:.2f}")

        # Top 5 servicios más contactados
        self.stdout.write("\n🏆 TOP 5 servicios con más solicitudes:")
        top = Service.objects.annotate(reqs=Count("requests")).order_by("-reqs")[:5]
        if top:
            for s in top:
                self.stdout.write(f"  - {s.title} → {s.reqs} solicitud(es)")
        else:
            self.stdout.write("  (No hay solicitudes registradas aún)")

        self.stdout.write("\n✅ Estadísticas generadas correctamente.")
