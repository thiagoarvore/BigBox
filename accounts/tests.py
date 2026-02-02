from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="pass123")

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(
            reverse("login"), {"username": "tester", "password": "pass123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))

    def test_login_failure(self):
        response = self.client.post(
            reverse("login"), {"username": "tester", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")

    def test_logout_redirect(self):
        self.client.login(username="tester", password="pass123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))
