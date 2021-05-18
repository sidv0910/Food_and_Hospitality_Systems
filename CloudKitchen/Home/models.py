from django.core.exceptions import ValidationError
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    contact = models.IntegerField()
    password = models.CharField(max_length=10)

class Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)

def shop_license_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Documents/{1}'.format(instance.restaurant_id, "Shop_License." + filename.split('.')[-1])

def fssai_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Documents/{1}'.format(instance.restaurant_id, "FSSAI." + filename.split('.')[-1])

def gstin_pan_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Documents/{1}'.format(instance.restaurant_id, "GSTIN_PAN." + filename.split('.')[-1])

def menu_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Documents/{1}'.format(instance.restaurant_id, "Menu." + filename.split('.')[-1])

def facade_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Images/{1}'.format(instance.restaurant_id, "Facade." + filename.split('.')[-1])

def kitchen_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Images/{1}'.format(instance.restaurant_id, "Kitchen." + filename.split('.')[-1])

def dining_packaging_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Images/{1}'.format(instance.restaurant_id, "Dining_Packaging." + filename.split('.')[-1])

def locality_directory_path(instance, filename):
    return 'Home/Restaurant/{0}/Images/{1}'.format(instance.restaurant_id, "Locality." + filename.split('.')[-1])

def vehicle_registration_certificate_directory_path(instance, filename):
    return 'Home/Delivery/{0}/{1}'.format(instance.delivery_id, "Vehicle_Registration_Certificate." + filename.split('.')[-1])

def driving_license_directory_path(instance, filename):
    return 'Home/Delivery/{0}/{1}'.format(instance.delivery_id, "Driving_License." + filename.split('.')[-1])

class Restaurant(models.Model):
    restaurant_id = models.CharField(max_length=6)
    restaurant_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    zip = models.IntegerField()
    restaurant_email = models.EmailField(primary_key=True)
    restaurant_contact = models.IntegerField()
    password = models.CharField(max_length=10)
    cost_for_two = models.DecimalField(max_digits=5, decimal_places=2)
    outlets = models.IntegerField()
    cuisine = models.CharField(max_length=100)
    working_days = models.CharField(max_length=100)
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()
    shop_license = models.FileField(upload_to=shop_license_directory_path)
    fssai = models.FileField(upload_to=fssai_directory_path)
    gstin_pan = models.FileField(upload_to=gstin_pan_directory_path)
    menu = models.FileField(upload_to=menu_directory_path)
    facade = models.ImageField(upload_to=facade_directory_path)
    kitchen = models.ImageField(upload_to=kitchen_directory_path)
    dining_packaging = models.ImageField(upload_to=dining_packaging_directory_path)
    locality = models.ImageField(upload_to=locality_directory_path)
    status = models.BooleanField(default=False)

class Delivery(models.Model):
    delivery_id = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=10)
    vehicle_model = models.CharField(max_length=50)
    vehicle_registration_certificate = models.FileField(upload_to=vehicle_registration_certificate_directory_path, blank=True, null=True)
    driving_license = models.FileField(upload_to=driving_license_directory_path, blank=True, null=True)
    status = models.BooleanField(default=False)

    def clean(self):
        emails = list(Restaurant.objects.values_list('restaurant_email', flat=True)) + list(User.objects.values_list('email', flat=True))
        if self.email in emails:
            raise ValidationError({'email': 'A Restaurant Account or an User Account already exists with the given Email'}, code='invalid')