from django import forms

from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit

from kitchen.models import (
    Dish,
    Ingredient,
    Cook
)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":
                "form-control",
                "placeholder":
                "Username"
            }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":
                "form-control",
                "placeholder":
                    "Password"
            }))
    remember_me = (forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="Remember Me"
    ))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit(
                "login",
                "Login",
                css_class="btn btn-primary"
            ))


class DishForm(forms.ModelForm):
    ingredients_text = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Write delicious ingredients for the dish please"}),
        label="Ingredients"
    )
    cooks_text = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Who will cook this dish?"}),
        label="Cooks"
    )
    description_text = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Describe the dish please"})
    )

    class Meta:
        model = Dish
        fields = [
            "name",
            "dish_type",
            "ingredients",
            "cooks_text",
            "description",
            "price"
        ]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]


class CookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = [
            "first_name",
            "last_name",
            "years_of_experience"
        ]
