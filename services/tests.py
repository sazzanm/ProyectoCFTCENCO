from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Service

class MarketplaceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # usuarios
        cls.user = User.objects.create_user(username="alice", password="s3cret")
        # categorías
        cls.cat1 = Category.objects.create(name="Limpieza")
        cls.cat2 = Category.objects.create(name="Electricidad")
        # servicio de ejemplo
        cls.svc = Service.objects.create(
            owner=cls.user,
            title="Limpieza de hogar",
            description="Ofrezco limpieza general",
            category=cls.cat1,
            price_from=25000,
            is_active=True,
        )

    def test_landing_ok(self):
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_home_list_ok(self):
        url = reverse("service_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Servicios")
        self.assertContains(resp, "Limpieza de hogar")

    def test_detail_requires_login(self):
        url = reverse("service_detail", args=[self.svc.pk])
        resp = self.client.get(url)
        # debe redirigir a login
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp.url)

    def test_detail_ok_logged_in(self):
        self.client.login(username="alice", password="s3cret")
        url = reverse("service_detail", args=[self.svc.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Limpieza de hogar")
        self.assertContains(resp, "Limpieza")

    def test_create_requires_login(self):
        url = reverse("service_new")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp.url)

    def test_create_service_logged_in(self):
        self.client.login(username="alice", password="s3cret")
        url = reverse("service_new")
        data = {
            "title": "Electricista domicilio",
            "description": "Instalaciones básicas",
            "category": self.cat2.id,
            "price_from": 40000,
            "is_active": True,
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Service.objects.count(), 2)

    def test_my_services_requires_login(self):
        url = reverse("my_services")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_my_services_ok(self):
        self.client.login(username="alice", password="s3cret")
        url = reverse("my_services")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Limpieza de hogar")
