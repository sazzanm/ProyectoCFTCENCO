from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from .models import Service, Category, ServiceRequest
from .forms import ServiceForm, ServiceRequestForm


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    paginate_by = 12

    def get_queryset(self):
        qs = (Service.objects
              .select_related("category", "owner")
              .filter(is_active=True)
              .order_by("-created_at"))
        q = self.request.GET.get("q")
        cat = self.request.GET.get("cat")
        if q:
            qs = qs.filter(title__icontains=q)
        if cat:
            qs = qs.filter(category__slug=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all().order_by("name")
        ctx["selected_cat"] = self.request.GET.get("cat")
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all().order_by("name")
        ctx["selected_cat"] = self.request.GET.get("cat")
        ctx["q"] = self.request.GET.get("q", "")
        # total robusto: si existe paginator úsalo, si no, cuenta el queryset
        ctx["total"] = ctx.get("paginator").count if ctx.get("paginator") else self.get_queryset().count()
        return ctx

class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = self.object
        user = self.request.user

        is_owner = user.is_authenticated and service.owner_id == user.id
        has_requested = (
            user.is_authenticated
            and service.requests.filter(requester=user).exists()
        )

        ctx.update({
            "is_owner": is_owner,
            "has_requested": has_requested,
            "requests_count": service.requests.count(),  # opcional para mostrar el total
        })
        return ctx

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "services/form.html"
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        messages.success(self.request, "Tu servicio fue publicado con éxito.")
        return super().form_valid(form)
    
class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = "services/request_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.service_obj = get_object_or_404(Service, pk=kwargs["pk"])
        if request.user.is_authenticated and self.service_obj.owner_id == request.user.id:
            messages.warning(request, "No puedes contactar tu propio servicio.")
            return redirect("service_detail", pk=self.service_obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.requester = self.request.user
        obj.service = self.service_obj
        try:
            obj.save()
            messages.success(self.request, "Solicitud enviada al proveedor.")   
        except IntegrityError:
            messages.info(self.request, "Ya habías enviado una solicitud a este servicio.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("service_detail", kwargs={"pk": self.service_obj.pk})


