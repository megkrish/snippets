from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menus", on_delete=models.CASCADE)
    cuisine_type = models.CharField(max_length=100)
    dish_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dish_name} - {self.price} ({self.cuisine_type})"