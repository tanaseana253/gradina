from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/images', null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_products', blank=True)
    cart = models.ManyToManyField(User, related_name='cart_products', blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_name = models.CharField(max_length=255, blank=True, null=True)
    delivery_phone = models.CharField(max_length=20, blank=True, null=True)
    save_for_next_order = models.BooleanField(default=False)  # New field to store the checkbox value
    old_cart = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


User._meta.get_field('email')._unique = True
