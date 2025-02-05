from django.test import TestCase, Client
from django.urls import reverse
from .models import Cook, Dish, Ingredient, DishType


class KitchenTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Cook.objects.create_user(username="testuser", password="testpass", first_name="Test",
                                             last_name="User")
        self.cook = Cook.objects.create(first_name="John", last_name="Doe")
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(name="Test Dish", description="Test Description", price=10.00,
                                        dish_type=self.dish_type)
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.dish.cooks.add(self.cook)

    def test_home_view(self):
        response = self.client.get(reverse("kitchen:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/home.html")

    def test_register_view(self):
        response = self.client.get(reverse("kitchen:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/register.html")

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("kitchen:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dashboard.html")

    def test_dishes_view(self):
        response = self.client.get(reverse("kitchen:dishes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dishes.html")

    def test_add_dish_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("kitchen:add_dish"), {
            "name": "New Dish",
            "description": "New Description",
            "price": 20.00,
            "dish_type": self.dish_type.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="New Dish").exists())

    def test_delete_dish_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("kitchen:delete_dish"), {
            "dish_id": self.dish.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())

    def test_cooks_view(self):
        response = self.client.get(reverse("kitchen:cooks"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cooks.html")

    def test_assigned_cooks_view(self):
        response = self.client.get(reverse("kitchen:assigned_cooks"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/assigned_cooks.html")

    def test_ingredients_view(self):
        response = self.client.get(reverse("kitchen:ingredients"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/ingredients.html")

    def test_add_ingredient_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("kitchen:add_ingredient"), {
            "name": "New Ingredient"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name="New Ingredient").exists())

    def test_delete_ingredient_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("kitchen:delete_ingredient"), {
            "ingredient_id": self.ingredient.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ingredient.objects.filter(id=self.ingredient.id).exists())

    def test_dishtypes_view(self):
        response = self.client.get(reverse("kitchen:dishtypes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dishtypes.html")

    def test_add_dishtype_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("kitchen:add_dishtype"), {
            "name": "New DishType"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DishType.objects.filter(name="New DishType").exists())

    def test_delete_dishtype_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("kitchen:delete_dishtype"), {
            "dishtype_id": self.dish_type.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DishType.objects.filter(id=self.dish_type.id).exists())
