from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Kit, Product


class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Cat")
        self.product = Product.objects.create(
            name="Prod",
            category=self.category,
            ativo=True,
            amount=5,
            premium=False,
            price=10.0,
            ncm=1,
        )
        self.kit = Kit.objects.create(cost=9.0, price=12.0, profit=3.0, label="Kit")
        self.kit.content.add(self.product)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Cat")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Prod R$ 10.0")

    def test_create_identical_kit(self):
        url = reverse("create_identical_kit", kwargs={"pk": self.kit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Kit.objects.count(), 2)
        new_kit = Kit.objects.latest("created_at")
        self.assertEqual(new_kit.label, self.kit.label)
        self.assertEqual(list(new_kit.content.all()), list(self.kit.content.all()))


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="pass")
        self.category = Category.objects.create(name="Cat")
        self.product1 = Product.objects.create(
            name="Prod1",
            category=self.category,
            ativo=True,
            amount=5,
            premium=False,
            price=4.0,
            ncm=2,
        )
        self.product2 = Product.objects.create(
            name="Another",
            category=self.category,
            ativo=True,
            amount=5,
            premium=False,
            price=6.0,
            ncm=3,
        )

    def test_products_list_search(self):
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse("products_list"), {"search": "Prod1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prod1")
        self.assertNotContains(response, "Another")

    def test_product_create_view(self):
        self.client.login(username="user", password="pass")
        data = {
            "name": "Created",
            "category": self.category.id,
            "ativo": True,
            "amount": 10,
            "premium": False,
            "price": 5.5,
            "ncm": 5,
        }
        response = self.client.post(reverse("new_product"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name="Created").exists())

    def test_create_kit_view(self):
        self.client.login(username="user", password="pass")
        data = {
            "label": "Kit1",
            f"product_{self.product1.id}": True,
            f"product_{self.product2.id}": True,
        }
        response = self.client.post(reverse("new_kit"), data)
        self.assertEqual(response.status_code, 302)
        kit = Kit.objects.get(label="Kit1")
        self.assertEqual(kit.content.count(), 2)
