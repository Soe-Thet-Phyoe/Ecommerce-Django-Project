from django.db import models
from django.contrib.auth.models import User
from apps.products.models import ProductModel

# Create your models here.

class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel)

    def __str__(self):
        return f"{self.user.username}'s cart"