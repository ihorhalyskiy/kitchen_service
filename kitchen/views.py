from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model
)
from django.core.paginator import Paginator
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404
)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView
)

from kitchen.forms import (
    UserLoginForm,
    DishForm,
    IngredientForm,
    CookForm
)
from kitchen.models import (
    Dish,
    Cook,
    Ingredient
)


def home(request):
    if request.user.is_authenticated:
        return redirect("kitchen:kitchen_info")

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
                return redirect("kitchen:kitchen_info")
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


User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if not User.objects.filter(
                    username=username
            ).exists():
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                user.save()
                login(request, user)
                return redirect("kitchen:kitchen_info")
            else:
                return render(
                    request,
                    "kitchen/register.html",
                    {"error": "Username already exists"}
                )

    return render(request, "kitchen/register.html")


class KitchenInfoView(ListView):

    model = Dish
    template_name = "kitchen/kitchen_info.html"
    context_object_name = "Information_page"
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            "cooks",
            "ingredients",
            "dish_type"
        ).order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["Information_page"] = page_obj
        return context


class DishesView(ListView):

    model = Dish
    template_name = "kitchen/dishes.html"
    context_object_name = "dishes_page"
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("dish_name")
        if query:
            return Dish.objects.filter(name__icontains=query).order_by("name")
        else:
            return Dish.objects.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("dish_name")
        return context


class DishCreateView(CreateView):

    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dishes")


class DishDeleteView(DeleteView):

    model = Dish
    template_name = "kitchen/dishes.html"
    success_url = reverse_lazy("kitchen:dishes")


class DishRemoveFromCookView(View):

    def post(self, request, dish_id, cook_id):
        dish = get_object_or_404(Dish, id=dish_id)
        cook = get_object_or_404(Cook, id=cook_id)
        cook.dishes.remove(dish)
        return redirect("kitchen:cooks")

    def get(self, request, dish_id, cook_id):
        dish = get_object_or_404(Dish, id=dish_id)
        cook = get_object_or_404(Cook, id=cook_id)
        return render(
            request,
            "kitchen/dishes.html",
            {"dish": dish, "cook": cook}
        )


class EditDishPriceView(UpdateView):

    model = Dish
    template_name = "kitchen/edit_dish_price.html"
    fields = ["price"]
    success_url = reverse_lazy("kitchen:dishes")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class IngredientsView(ListView):
    model = Ingredient
    template_name = "kitchen/ingredients.html"
    context_object_name = "ingredients_page"
    paginate_by = 24

    def get_queryset(self):
        query = self.request.GET.get("ingredient_name")
        if query:
            return Ingredient.objects.filter(
                name__icontains=query
            ).order_by("name")
        else:
            return Ingredient.objects.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("ingredient_name")
        return context


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/create_ingredient.html"
    success_url = reverse_lazy("kitchen:ingredients")


class IngredientDeleteView(View):
    def post(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("ingredient_id")
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        ingredient.delete()
        return redirect("kitchen:ingredients")


class IngredientDeleteInDishesView(View):
    def post(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("id")
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        dishes = Dish.objects.filter(ingredients=ingredient)
        for dish in dishes:
            dish.ingredients.remove(ingredient)
        return redirect(request.META.get(
            "HTTP_REFERER",
            "redirect_if_referer_not_found")
        )

    def get(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("id")
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        return render(
            request,
            "kitchen/ingredients.html",
            {"ingredient": ingredient}
        )


class CreateIngredientInDishesView(View):
    def post(self, request, *args, **kwargs):
        dish_id = kwargs.get("id")
        dish = get_object_or_404(Dish, id=dish_id)
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            dish.ingredients.add(ingredient)
            return redirect("kitchen:dishes")
        return render(
            request,
            "kitchen/create_ingredient_in_dishes.html",
            {"form": form, "dish": dish}
        )

    def get(self, request, *args, **kwargs):
        dish_id = kwargs.get("id")
        dish = get_object_or_404(Dish, id=dish_id)
        form = IngredientForm()
        return render(
            request,
            "kitchen/create_ingredient_in_dishes.html",
            {"form": form, "dish": dish}
        )


class CookListView(ListView):
    model = Cook
    template_name = "kitchen/cooks.html"
    context_object_name = "cook_list"
    paginate_by = 8

    def get_queryset(self):
        full_name = self.request.GET.get("full_name")
        queryset = super().get_queryset()
        if full_name:
            queryset = queryset.annotate(
                full_name=Concat(
                    "first_name", Value(" "),
                    "last_name", output_field=CharField()
                )
            ).filter(full_name__icontains=full_name)
        return queryset.filter(
            years_of_experience__gt=0
        ).order_by("first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("full_name", "")
        return context


class CookCreateView(View):
    def post(self, request, *args, **kwargs):
        form = CookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("kitchen:cooks")
        return render(
            request,
            "kitchen/cook_form.html",
            {"form": form}
        )

    def get(self, request, *args, **kwargs):
        form = CookForm()
        return render(
            request,
            "kitchen/cook_form.html",
            {"form": form}
        )


class CookDeleteView(View):
    def post(self, request, *args, **kwargs):
        cook_id = kwargs.get("id")
        cook = get_object_or_404(Cook, id=cook_id)
        cook.delete()
        return redirect("kitchen:cooks")

    def get(self, request, *args, **kwargs):
        return render(request, "kitchen/cooks.html")


class AddDishToCookView(View):
    def post(self, request, *args, **kwargs):
        cook_id = kwargs.get("cook_id")
        cook = get_object_or_404(Cook, id=cook_id)
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save()
            cook.dishes.add(dish)
            return redirect("kitchen:cooks")
        return render(
            request,
            "kitchen/add_dish_to_cook.html",
            {"form": form, "cook": cook}
        )

    def get(self, request, *args, **kwargs):
        cook_id = kwargs.get("cook_id")
        cook = get_object_or_404(Cook, id=cook_id)
        form = DishForm()
        return render(
            request,
            "kitchen/add_dish_to_cook.html",
            {"form": form, "cook": cook}
        )
