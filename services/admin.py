from django.contrib import admin
from django.db.models import Count
from .models import Category, Service, ServiceRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "service_count")  # ← mostrará el total
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_service_count=Count("services"))  # annotate: evita N+1 consultas

    def service_count(self, obj):
        return obj._service_count
    service_count.short_description = "Servicios"
    service_count.admin_order_field = "_service_count"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description", "owner__username")
    date_hierarchy = "created_at"       # navegación por fecha arriba
    ordering = ("-created_at",)         # los más nuevos primero
    list_per_page = 25                  # paginación cómoda

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("service", "requester", "created_at")
    search_fields = ("service__title", "requester__username")