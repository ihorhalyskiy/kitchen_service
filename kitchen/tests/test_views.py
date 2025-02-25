from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen.models import Dish, DishType, Ingredient

User = get_user_model()

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("kitchen:home")

    def test_home_view_unauthenticated(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/home.html")

    def test_home_view_authenticated(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse("kitchen:kitchen_info"))


class KitchenInfoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.kitchen_info_url = reverse("kitchen:kitchen_info")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_kitchen_info_view(self):
        response = self.client.get(self.kitchen_info_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/kitchen_info.html")


class DishesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dishes_url = reverse("kitchen:dishes")
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient = Ingredient.objects.create(name="Tomato")
        self.dish = Dish.objects.create(
            name="Pizza",
            description="A delicious pizza",
            price=12.99,
            dish_type=self.dish_type
        )
        self.dish.ingredients.add(self.ingredient)

    def test_dishes_view(self):
        response = self.client.get(self.dishes_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dishes.html")
        self.assertContains(response, "Pizza")


class DishCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dish_create_url = reverse("kitchen:dishes_create")
        self.dish_type = DishType.objects.create(name="Dessert")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_dish_create_view_get(self):
        response = self.client.get(self.dish_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")


class CookListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cooks_url = reverse("kitchen:cooks")
        self.user = User.objects.create_user(
            username="testcook",
            password="testpassword",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5
        )
        self.client.login(username="testcook", password="testpassword")

    def test_cook_list_view(self):
        response = self.client.get(self.cooks_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cooks.html")
        self.assertContains(response, "Test Cook")


class CookCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cook_create_url = reverse("kitchen:cooks_create")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_cook_create_view_get(self):
        response = self.client.get(self.cook_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_form.html")


