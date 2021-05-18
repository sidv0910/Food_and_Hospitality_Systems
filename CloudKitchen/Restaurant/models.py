from django.db import models
from Home.models import Restaurant, User, Delivery
from User.models import Address

class Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)

class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

    class Meta:
        unique_together = (("restaurant", "category"))

    def __unicode__(self):
        return u'%s' % (self.category)

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=100)
    item_type = models.CharField(max_length=7)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Orders(models.Model):
    order_number = models.IntegerField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    items = models.CharField(max_length=500)
    quantity = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    delivery = models.CharField(max_length=6, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    food_is_being_prepared = models.BooleanField(default=False)
    ready_for_delivery = models.BooleanField(default=False)
    picked_up = models.BooleanField(default=False)
    out_for_delivery = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    date = models.DateField(default="2020-01-01")
    time = models.TimeField(default="00:00:00")