from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from services.views import (
    LandingView,
    ServiceListView,
    ServiceDetailView,
    ServiceCreateView,
    ServiceRequestCreateView,
    MyServicesView,
    SignUpView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("accounts/login/",  auth_views.LoginView.as_view(),  name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),

    # Landing y catálogo
    path("", LandingView.as_view(), name="home"),
    path("servicios/", ServiceListView.as_view(), name="service_list"),

    # Servicios
    path("servicios/nuevo/", ServiceCreateView.as_view(), name="service_new"),
    path("servicios/<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("servicios/<int:pk>/contactar/", ServiceRequestCreateView.as_view(), name="service_contact"),

    # Panel personal
    path("mis-servicios/", MyServicesView.as_view(), name="my_services"),
]
