from django.db import models
from Home.models import User, Restaurant, Delivery
from Restaurant.models import Category, Item

class Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()