from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "dish type"
        verbose_name_plural = "dish types"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    ingredients = models.ManyToManyField(Ingredient)
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
