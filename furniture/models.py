from django.db import models
from django.conf import settings


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('furniture', 'Furniture'),
        ('decor', 'Decor'),
        ('lighting', 'Lighting'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='furniture')
    subcategory = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color1 = models.CharField(max_length=20, blank=True)  
    color2 = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg')
    brand = models.CharField(max_length=100, blank=True)
    in_stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

class Room(models.Model):
    room_name = models.CharField(max_length=100)


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='subcategories/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


