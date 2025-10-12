from django.db import models
from django.contrib.auth.models import User          # ← usamos el User nativo de Django
from django.utils.text import slugify                # ← para crear slugs de categorías

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)  # ← nombre visible (ej. Gasfitería)
    slug = models.SlugField(max_length=90, unique=True, blank=True)  # ← para filtrar por URL

    def save(self, *args, **kwargs):
        if not self.slug:                              # ← si no hay slug, lo generamos a partir del name
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Service(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")
    # ↑ dueño de la publicación; si el usuario se borra, se borran sus servicios
    title = models.CharField(max_length=120)           # ← título de la publicación
    description = models.TextField()                   # ← descripción
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="services")
    # ↑ PROTECT: no deja borrar una categoría si tiene servicios
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)      # ← permite ocultar/pausar un servicio
    created_at = models.DateTimeField(auto_now_add=True)  # ← fecha de creación automática

    def __str__(self):
        return self.title
    
class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="requests")
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_requests")
    message = models.TextField(blank=True)  # mensaje opcional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["service", "requester"],
                name="uniq_service_request_per_user",
            )
        ]

    def __str__(self):  
        return f"Req({self.requester.username} → {self.service.title})"
    
