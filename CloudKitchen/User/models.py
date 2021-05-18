from django.db import models
from Home.models import User

class Address(models.Model):
    address_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    landmark = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    zip = models.IntegerField()

class Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)