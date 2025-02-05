from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cook, Dish, Ingredient, DishType
from django.shortcuts import get_object_or_404
from .forms import UserLoginForm


def home(request):
    if request.user.is_authenticated:
        return redirect("kitchen:dashboard")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(0)
                return redirect("kitchen:dashboard")
            else:
                messages.error(
                    request,
                    "Invalid credentials. Please try again."
                )
        else:
            messages.error(
                request,
                "Form is not valid. Please try again."
            )
    else:
        form = UserLoginForm()
    return render(
        request,
        "kitchen/home.html",
        {"form": form}
    )


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                user.save()
                return redirect("home")
            else:
                return render(
                    request,
                    "kitchen/register.html",
                    {"error": "Username already exists"}
                )
    return render(
        request,
        "kitchen/register.html"
    )


def dashboard(request):
    dishes = Dish.objects.all()
    cooks = Cook.objects.all()
    ingredients = Ingredient.objects.all()

    context = {
        "dishes": dishes,
        "cooks": cooks,
        "ingredients": ingredients,
    }
    return render(
        request,
        "kitchen/dashboard.html",
        context
    )


def kitchen_info(request):
    dishes_list = Dish.objects.prefetch_related(
        "cooks", "ingredients", "dish_type"
    ).order_by("name")
    paginator = Paginator(dishes_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(
        request,
        "kitchen/kitchen_info.html",
        context
    )


def achievements(request):
    return render(
        request,
        "kitchen/achievements.html"
    )


def dishes(request):
    dishes_list = Dish.objects.order_by("name")
    paginator = Paginator(dishes_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "kitchen/dishes.html",
        {"page_obj": page_obj}
    )


def add_dish(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        dish_type_id = request.POST.get("dish_type")
        dish_type = DishType.objects.get(id=dish_type_id)
        dish = Dish(
            name=name,
            description=description,
            price=price,
            dish_type=dish_type
        )
        dish.save()
        return redirect("kitchen:dashboard")
    dish_types = DishType.objects.all()
    return render(
        request,
        "kitchen/add_dish.html",
        {"dish_types": dish_types}
    )


def delete_dish(request):
    dishes = Dish.objects.all()
    if request.method == "POST":
        dish_id = request.POST.get("dish_id")
        dish = Dish.objects.get(id=dish_id)
        dish.delete()
        return redirect("kitchen:dashboard")
    return render(
        request,
        "kitchen/delete_dish.html",
        {"dishes": dishes}
    )


def delete_dish_list(request):
    dishes = Dish.objects.all()
    return render(
        request,
        "kitchen/delete_dish.html",
        {"dishes": dishes}
    )


def cooks(request):
    cooks_list = Cook.objects.exclude(
        first_name__isnull=True).exclude(
        first_name__exact='').order_by(
        "first_name"
    )
    paginator = Paginator(cooks_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "kitchen/cooks.html",
        {"page_obj": page_obj}
    )


def assigned_cooks(request):
    assigned_cooks_list = Cook.objects.filter(
        dishes__isnull=False
    ).distinct().order_by(
        "first_name"
    )
    paginator = Paginator(assigned_cooks_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "assigned_cooks": page_obj,
    }
    return render(
        request,
        "kitchen/assigned_cooks.html",
        context
    )


def add_assigned_cook(request):
    if request.method == "POST":
        cook_id = request.POST.get("cook_id")
        dish_id = request.POST.get("dish_id")
        cook = Cook.objects.get(id=cook_id)
        dish = Dish.objects.get(id=dish_id)
        dish.cooks.add(cook)
        return redirect("kitchen:assigned_cooks")
    cooks = Cook.objects.all()
    dishes = Dish.objects.all()
    context = {
        "cooks": cooks,
        "dishes": dishes,
    }
    return render(
        request,
        "kitchen/add_assigned_cook.html",
        context
    )


def delete_assigned_cook(request):
    if request.method == "POST":
        cook_id = request.POST.get("cook_id")
        dish_id = request.POST.get("dish_id")
        cook = Cook.objects.get(id=cook_id)
        dish = Dish.objects.get(id=dish_id)
        dish.cooks.remove(cook)
        return redirect("kitchen:assigned_cooks")
    assigned_cooks = Cook.objects.filter(dishes__isnull=False).distinct()
    context = {"assigned_cooks": assigned_cooks}
    return render(
        request,
        "kitchen/delete_assigned_cook.html",
        context
    )


def remove_cook_from_dish(request, dish_id, cook_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cook = get_object_or_404(Cook, id=cook_id)
    dish.cooks.remove(cook)
    return redirect("kitchen:view_assigned_cooks")


def assign_cooks(request):
    if request.method == "POST":
        dish_id = request.POST.get("dish")
        cook_ids = request.POST.getlist("cooks")

        dish = Dish.objects.get(id=dish_id)
        cooks = Cook.objects.filter(id__in=cook_ids)

        dish.cooks.set(cooks)
        return redirect("kitchen:dashboard")

    return redirect("kitchen:dashboard")


def view_assigned_cooks(request):
    dish_list = Dish.objects.prefetch_related(
        "cooks",
        "ingredients",
        "dish_type"
    ).order_by("name").all()
    paginator = Paginator(dish_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(
        request,
        "kitchen/view_assigned_cooks.html",
        context
    )


def delete_assign_cook_to_dishes(request):
    if request.method == "POST":
        dish_id = request.POST.get("dish_id")
        cook_ids = request.POST.getlist("cook_ids")
        dish = Dish.objects.get(id=dish_id)
        cooks = Cook.objects.filter(id__in=cook_ids)
        dish.cooks.remove(*cooks)
        return redirect("kitchen:dashboard")
    dishes = Dish.objects.all()
    cooks = Cook.objects.all()
    context = {
        "dishes": dishes,
        "cooks": cooks,
    }
    return render(
        request,
        "kitchen/delete_assign_cook_to_dishes.html",
        context
    )


def ingredients(request):
    ingredients_list = Ingredient.objects.order_by("name")
    paginator = Paginator(ingredients_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "kitchen/ingredients.html",
        {"page_obj": page_obj}
    )


def add_ingredient(request):
    if request.method == "POST":
        name = request.POST.get("name")
        ingredient = Ingredient(name=name)
        ingredient.save()
        return redirect("kitchen:dashboard")
    return render(
        request,
        "kitchen/add_ingredient.html"
    )


def delete_ingredient(request):
    ingredients = Ingredient.objects.all()
    if request.method == "POST":
        ingredient_id = request.POST.get("ingredient_id")
        ingredient = Ingredient.objects.get(id=ingredient_id)
        ingredient.delete()
        return redirect("kitchen:dashboard")
    return render(
        request, "kitchen/delete_ingredient.html",
        {"ingredients": ingredients}
    )


def delete_ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(
        request, "kitchen/delete_ingredient.html",
        {"ingredients": ingredients}
    )


def add_dishtype(request):
    if request.method == "POST":
        name = request.POST.get("name")
        dishtype = DishType(name=name)
        dishtype.save()
        return redirect("kitchen:dashboard")
    return render(
        request, "kitchen/add_dishtype.html"
    )


def delete_dishtype(request):
    dishtypes = DishType.objects.all()
    if request.method == "POST":
        dishtype_id = request.POST.get("dishtype_id")
        dishtype = DishType.objects.get(id=dishtype_id)
        dishtype.delete()
        return redirect("kitchen:dashboard")
    return render(
        request, "kitchen/delete_dishtype.html",
        {"dishtypes": dishtypes}
    )


def delete_dishtype_list(request):
    dishtypes = DishType.objects.all()
    return render(
        request, "kitchen/delete_dishtype.html",
        {"dishtypes": dishtypes}
    )


def dishtypes(request):
    dishtypes_list = DishType.objects.all()
    context = {"dishtypes": dishtypes_list}
    return render(
        request, "kitchen/dishtypes.html", context
    )
