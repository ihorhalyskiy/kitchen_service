from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "kitchen"

urlpatterns = [
    path(
        "", views.home,
        name="home"
         ),
    path(
        "register/", views.register,
        name="register"
    ),
    path(
        "dishes/", views.dishes,
        name="dishes"
    ),
    path(
        "cooks/", views.cooks,
        name="cooks"
    ),
    path(
        "ingredients/", views.ingredients,
        name="ingredients"
    ),
    path(
        "dashboard/", views.dashboard,
        name="dashboard"
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(),
        name="logout"
    ),
    path(
        "add_dish/", views.add_dish,
        name="add_dish"
    ),
    path(
        "delete_dish/", views.delete_dish,
        name="delete_dish"
    ),
    path(
        "delete_dish_list/", views.delete_dish_list,
        name="delete_dish_list"
    ),
    path(
        "add_ingredient/", views.add_ingredient,
        name="add_ingredient"
    ),
    path(
        "delete_ingredient/", views.delete_ingredient,
        name="delete_ingredient"
    ),
    path(
        "delete_ingredient_list/", views.delete_ingredient_list,
        name="delete_ingredient_list"
    ),
    path(
        "add_dishtype/", views.add_dishtype,
        name="add_dishtype"
    ),
    path(
        "delete_dishtype/", views.delete_dishtype,
        name="delete_dishtype"
    ),
    path(
        "delete_dishtype_list/", views.delete_dishtype_list,
        name="delete_dishtype_list"
    ),
    path(
        "dishtypes/", views.dishtypes,
        name="dishtypes"
    ),
    path(
        "assigned_cooks/", views.assigned_cooks,
        name="assigned_cooks"
    ),
    path(
        "add_assigned_cook/", views.add_assigned_cook,
        name="add_assigned_cook"
    ),
    path(
        "delete_assigned_cook/", views.delete_assigned_cook,
        name="delete_assigned_cook"
    ),
    path(
        "kitchen_info/", views.kitchen_info,
        name="kitchen_info"
    ),
    path(
        "achievements/", views.achievements,
        name="achievements"
    ),
]
