"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from services.views import ServiceListView, ServiceDetailView, ServiceCreateView,  ServiceRequestCreateView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/login/",  auth_views.LoginView.as_view(),  name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", ServiceListView.as_view(), name="home"),
    path("services/new/", ServiceCreateView.as_view(), name="service_new"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("services/<int:pk>/contact/", ServiceRequestCreateView.as_view(), name="service_contact"),
]

