from django.conf import settings
from django.db import models


class FoodEntry(models.Model):
    name = models.CharField(max_length=100)
    favorite_dish = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="food_entries",
    )

    def __str__(self):
        return f"{self.name} — {self.favorite_dish}"
