from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cook, DishType, Ingredient, Dish


class CookAdminForm(forms.ModelForm):
    years_of_experience = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 11)],
        widget=forms.Select
    )

    class Meta:
        model = Cook
        fields = "__all__"


class CookAdmin(UserAdmin):
    form = CookAdminForm
    list_display = (
        "username",
        "years_of_experience",
        "first_name",
        "last_name",
        "email"
    )
    ordering = (
        "first_name",
        "last_name",
    )
    list_filter = ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("years_of_experience",)}),
    )


class DishAdmin(admin.ModelAdmin):
    filter_horizontal = ("ingredients", "cooks")
    list_display = (
        "name",
        "price",
        "description",
        "dish_type",
    )


admin.site.register(Cook, CookAdmin)
admin.site.register(DishType)
admin.site.register(Ingredient)
admin.site.register(Dish, DishAdmin)
