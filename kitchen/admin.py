from django.contrib import admin
from .models import Cook, DishType, Ingredient, Dish

class CookAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "years_of_experience",
        "get_first_name",
        "get_last_name",
        "get_email"
    )
    ordering = (
        "user__first_name",
        "user__last_name",
    )
    list_filter = ("years_of_experience",)

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "First Name"
    get_first_name.admin_order_field = "user__first_name"

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = "Last Name"
    get_last_name.admin_order_field = "user__last_name"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"

admin.site.register(Cook, CookAdmin)
admin.site.register(DishType)
admin.site.register(Ingredient)
admin.site.register(Dish)
