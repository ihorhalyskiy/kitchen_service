from django.test import TestCase
from django.contrib.auth import get_user_model
from kitchen.models import DishType, Ingredient, Dish


User = get_user_model()


class CookModelTest(TestCase):
    def setUp(self):
        self.cook = User.objects.create_user(
            username="testcook",
            password="testpassword",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5
        )

    def test_cook_creation(self):
        self.assertEqual(self.cook.username, "testcook")
        self.assertEqual(self.cook.first_name, "Test")
        self.assertEqual(self.cook.last_name, "Cook")
        self.assertEqual(self.cook.years_of_experience, 5)
        self.assertTrue(self.cook.check_password("testpassword"))

    def test_cook_str(self):
        self.assertEqual(str(self.cook), "Test Cook")


class DishTypeModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")

    def test_dish_type_creation(self):
        self.assertEqual(self.dish_type.name, "Main Course")

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), "Main Course")


class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato")

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, "Tomato")

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), "Tomato")


class DishModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Dessert")
        self.ingredient = Ingredient.objects.create(name="Sugar")
        self.cook = User.objects.create_user(
            username="testcook2",
            password="testpassword2",
            first_name="Test2",
            last_name="Cook2",
            years_of_experience=3
        )
        self.dish = Dish.objects.create(
            name="Cake",
            description="A sweet dessert",
            price=10.99,
            dish_type=self.dish_type
        )
        self.dish.ingredients.add(self.ingredient)
        self.dish.cooks.add(self.cook)

    def test_dish_creation(self):
        self.assertEqual(self.dish.name, "Cake")
        self.assertEqual(self.dish.description, "A sweet dessert")
        self.assertEqual(self.dish.price, 10.99)
        self.assertEqual(self.dish.dish_type, self.dish_type)
        self.assertIn(self.ingredient, self.dish.ingredients.all())
        self.assertIn(self.cook, self.dish.cooks.all())

    def test_dish_str(self):
        self.assertEqual(str(self.dish), "Cake")
