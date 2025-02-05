from django.test import TestCase
from django.contrib.auth import get_user_model
from kitchen.models import Cook, Dish, Ingredient, DishType


class CookModelTests(TestCase):

    def setUp(self):
        self.cook = get_user_model().objects.create(
            username="cookuser",
            password="testpass",
            first_name="Jane",
            last_name="Doe"
        )

        Cook.objects.filter(username="cookuser").update(years_of_experience=5)
        self.cook.refresh_from_db()

    def test_cook_creation(self):
        self.assertEqual(self.cook.username, "cookuser")
        self.assertEqual(self.cook.first_name, "Jane")
        self.assertEqual(self.cook.last_name, "Doe")
        self.assertEqual(self.cook.years_of_experience, 5)

    def test_cook_str(self):
        self.assertEqual(str(self.cook), "Jane Doe")


class DishTypeModelTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Dessert")

    def test_dishtype_creation(self):
        self.assertEqual(self.dish_type.name, "Dessert")

    def test_dishtype_str(self):
        self.assertEqual(str(self.dish_type), "Dessert")


class IngredientModelTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Sugar")

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, "Sugar")

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), "Sugar")


class DishModelTests(TestCase):

    def setUp(self):
        self.cook = get_user_model().objects.create(
            username="cookuser",
            password="testpass",
            first_name="Jane",
            last_name="Doe"
        )
        self.dish_type = DishType.objects.create(name="Dessert")
        self.ingredient = Ingredient.objects.create(name="Sugar")
        self.dish = Dish.objects.create(
            name="Cake",
            description="Delicious cake",
            price=15.00,
            dish_type=self.dish_type
        )
        self.dish.ingredients.add(self.ingredient)
        self.dish.cooks.add(self.cook)

    def test_dish_creation(self):
        self.assertEqual(self.dish.name, "Cake")
        self.assertEqual(self.dish.description, "Delicious cake")
        self.assertEqual(self.dish.price, 15.00)
        self.assertEqual(self.dish.dish_type, self.dish_type)

    def test_dish_ingredients(self):
        self.assertIn(self.ingredient, self.dish.ingredients.all())

    def test_dish_cooks(self):
        self.assertIn(self.cook, self.dish.cooks.all())

    def test_dish_str(self):
        self.assertEqual(str(self.dish), "Cake")
