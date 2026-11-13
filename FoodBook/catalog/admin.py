from django.contrib import admin
from .models import FoodEntry


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "favorite_dish", "owner", "created_at")
    list_filter = ("owner", "created_at")
    search_fields = ("name", "favorite_dish", "owner__username")
