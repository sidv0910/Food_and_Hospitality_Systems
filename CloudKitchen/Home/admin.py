import shutil, string, random

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings

from .models import User, Query, Restaurant, Delivery

class userInfo(admin.ModelAdmin):
    list_display = ('email', 'name', 'contact')

admin.site.register(User, userInfo)

class queryInfo(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email')

admin.site.register(Query, queryInfo)

class adminInfo(admin.ModelAdmin):
    model = Restaurant
    actions = ['delete_model']

    list_display = (
        'restaurant_name',
        'restaurant_email',
        'restaurant_contact',
        'restaurant_address',
        'account_actions',
    )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(obj)
            shutil.rmtree('Home/Restaurant/{0}/'.format(obj.restaurant_id))
        queryset.delete()

    def delete_model(self, request, obj):
        obj.delete()
        shutil.rmtree('Home/Restaurant/{0}/'.format(obj.restaurant_id))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<restaurant_id>.+)/accept/$',
                self.admin_site.admin_view(self.acceptApplication),
                name='Accept',
            ),
            url(
                r'^(?P<restaurant_id>.+)/decline/$',
                self.admin_site.admin_view(self.declineApplication),
                name='Decline',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        if obj.status == False:
            return format_html(
                '<a class="button" href="{}">&#10003; Accept</a>&nbsp;&nbsp;&nbsp;'
                '<a class="button" href="{}">&#10006; Decline</a>',
                reverse('admin:Accept', args=[obj.restaurant_id]),
                reverse('admin:Decline', args=[obj.restaurant_id]),
            )
    def restaurant_address(self, obj):
        return format_html(obj.address + ", " + obj.city + " - " + str(obj.zip))

    def acceptApplication(self, request, restaurant_id, *args, **kwargs):
        obj = Restaurant.objects.get(restaurant_id=restaurant_id)
        obj.status = True
        obj.save()
        subject = "Restaurant Registration Successful"
        message = obj.restaurant_name + ",\n\nCongratulations! Your restaurant has been successfully registered to Cloud Kitchen.\n\nYour Restaurant ID is " + obj.restaurant_id + ".\n(Note: Use this ID while signing in to your account.)\n\nYou can go live now and accept orders from the customers.\n\nThank You,\nCloud Kitchen Team"
        to = [obj.restaurant_email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, to)
        return HttpResponseRedirect('/admin/Home/restaurant/')

    def declineApplication(self, request, restaurant_id, *args, **kwargs):
        obj = Restaurant.objects.get(restaurant_id=restaurant_id)
        subject = "Restaurant Registration Failed"
        message = obj.restaurant_name + ",\n\nSorry! Your restaurant can not be registered to Cloud Kitchen.\nThis might be due to some errors in your Application or the files which you have submitted for registration from our website.\n\nKindly contact our team at cloudkitchen356@gmail.com to know the errors in your application, so that you can again submit the application free of errors.\n\nThank You,\nCloud Kitchen Team"
        to = [obj.restaurant_email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, to)
        self.delete_model(request, obj)
        return HttpResponseRedirect('/admin/Home/restaurant/')

admin.site.register(Restaurant, adminInfo)

class deliveryAdminInfo(admin.ModelAdmin):
    model = Delivery
    actions = ['delete_model']

    list_display = (
        'delivery_id',
        'name',
        'contact',
        'address',
        'vehicle_type',
        'vehicle_model',
    )

    def get_changeform_initial_data(self, request):
        ids = list(Delivery.objects.values_list('delivery_id', flat=True))
        passwords = list(Delivery.objects.values_list('password', flat=True))
        id_select, password_select = "", ""
        while True:
            id = "D" + str(randint(10000, 99999))
            if id not in ids:
                id_select = id
                break
        while True:
            password = ''.join(random.choice(string.ascii_uppercase) for x in range(1)) + ''.join(random.choice(string.ascii_lowercase) for x in range(3)) + random.choice(['@', '#', '$', '&']) + str(randint(1000, 9999))
            if password not in passwords:
                password_select = password
                break
        return {'delivery_id': id_select, 'password': password_select}

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(obj)
            shutil.rmtree('Home/Delivery/{0}/'.format(obj.delivery_id))
        queryset.delete()

    def delete_model(self, request, obj):
        obj.delete()
        shutil.rmtree('Home/Delivery/{0}/'.format(obj.delivery_id))

admin.site.register(Delivery, deliveryAdminInfo)