from django import forms
from .models import Service
from .models import ServiceRequest

# ModelForm: crea un formulario HTML a partir del modelo Service
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service                      # El modelo que “mapea” el form
        fields = ["title", "description",    # Campos que el usuario podrá completar
                  "category", "price_from", "is_active"]
        # Opcional: personalizar etiquetas o widgets
        labels = {
            "title": "Título del servicio",
            "description": "Descripción",
            "category": "Categoría",
            "price_from": "Precio desde",
            "is_active": "Visible",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["message"]
        labels = {"message": "Mensaje (opcional)"}
        widgets = {"message": forms.Textarea(attrs={"rows": 3})}