from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from .models import Service, Category, ServiceRequest
from .forms import ServiceForm, ServiceRequestForm


class LandingView(ListView):
    """Landing page con categorías y servicios recientes."""
    model = Service
    template_name = "services/landing.html"

    def get_queryset(self):
        return (Service.objects
                .select_related("category", "owner")
                .filter(is_active=True)
                .order_by("-created_at")[:6])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all().order_by("name")
        ctx["recent_services"] = self.get_queryset()
        ctx["total_services"] = Service.objects.filter(is_active=True).count()
        ctx["total_categories"] = Category.objects.count()
        return ctx


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
        ctx["total"] = ctx.get("paginator").count if ctx.get("paginator") else self.get_queryset().count()
        return ctx


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = "services/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = self.object
        user = self.request.user

        is_owner = user.is_authenticated and service.owner_id == user.id
        has_requested = (user.is_authenticated
                         and service.requests.filter(requester=user).exists())
        ctx.update({
            "is_owner": is_owner,
            "has_requested": has_requested,
            "requests_count": service.requests.count(),
        })
        return ctx


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "services/form.html"
    success_url = reverse_lazy("service_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        messages.success(self.request, "Tu servicio fue publicado con éxito.")
        return redirect(self.success_url)


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
        return redirect("service_detail", pk=self.service_obj.pk)


class MyServicesView(LoginRequiredMixin, ListView):
    """Vista personal: servicios del usuario y solicitudes recibidas."""
    model = Service
    template_name = "services/my_services.html"

    def get_queryset(self):
        return (Service.objects
                .select_related("category")
                .filter(owner=self.request.user)
                .order_by("-created_at"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["requests_received"] = (ServiceRequest.objects
                                    .select_related("service", "requester")
                                    .filter(service__owner=self.request.user)
                                    .order_by("-created_at")[:20])
        return ctx


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "Cuenta creada e inicio de sesión exitoso.")
        next_url = self.request.POST.get("next") or self.request.GET.get("next") or reverse("home")
        return redirect(next_url)