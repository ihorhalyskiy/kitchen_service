from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

from .views import (
    CookListView,
    KitchenInfoView,
    DishesView,
    DishCreateView,
    DishDeleteView,
    DishRemoveFromCookView,
    EditDishPriceView,
    IngredientsView,
    IngredientCreateView,
    IngredientDeleteView,
    IngredientDeleteInDishesView,
    CreateIngredientInDishesView,
    CookCreateView,
    CookDeleteView,
    AddDishToCookView
)

app_name = "kitchen"

urlpatterns = [
    path(
        "", views.home,
        name="home"
    ),
    path(
        "register/",
        views.register,
        name="register"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
    path(
        "kitchen_info/",
        KitchenInfoView.as_view(),
        name="kitchen_info"
    ),  # інформація про кухню
    path(
        "dishes/",
        DishesView.as_view(),
        name="dishes"
    ),  # сторінка страв
    path(
        "dishes/create/",
        DishCreateView.as_view(),
        name="dishes_create"
    ),  # сторінка створення нової страви
    path(
        "dishes/delete/<int:id>/",
        DishDeleteView.as_view(),
        name="dish_delete"
    ),  # видалення страви
    path(
        "dish/edit_price/<int:pk>/",
        EditDishPriceView.as_view(),
        name="edit_dish_price"
    ),  # Шлях для редагування ціни страви
    path(
        "dishes/create_ingredient/<int:id>/",
        CreateIngredientInDishesView.as_view(),
        name="create_ingredient_in_dishes"
    ),  # додавання інгредієнтів до страв
    path(
        "dish/remove/<int:dish_id>/from_cook/<int:cook_id>/",
        DishRemoveFromCookView.as_view(),
        name="dish_remove_from_cook"
    ),  # видалення страв у кухарів
    path(
        "cooks/",
        CookListView.as_view(),
        name="cooks"
    ),  # сторінка кухарів
    path(
        "cooks/create/",
        CookCreateView.as_view(),
        name="cooks_create"
    ),  # створення нового кухаря
    path(
        "cooks/delete/<int:id>/",
        CookDeleteView.as_view(),
        name="cook_delete"
    ),  # видалення кухаря
    path(
        "cook/<int:cook_id>/add_dish/",
        AddDishToCookView.as_view(),
        name="add_dish_to_cook"
    ),  # додавання страви до кухаря
    path(
        "ingredients/",
        IngredientsView.as_view(),
        name="ingredients"
    ),  # сторінка інгредієнтів
    path(
        "ingredients/create/",
        IngredientCreateView.as_view(),
        name="ingredients_create"
    ),  # сторінка створення нового інгредієнта
    path(
        "ingredients/delete/in-dish<int:id>/",
        IngredientDeleteInDishesView.as_view(),
        name="ingredient_delete"
    ),  # видалення інгредієнтів у стравах
    path(
        "ingredients/delete/<int:ingredient_id>/",
        IngredientDeleteView.as_view(),
        name="delete_specific_ingredient"
    ),  # видалення інгредієнта на сторінці інгредієнтів
]
