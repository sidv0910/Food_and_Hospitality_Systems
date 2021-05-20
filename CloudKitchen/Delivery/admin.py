from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Query, Cart
from Home.models import User, Restaurant, Delivery
from Restaurant.models import Category, Item

class queryInfo(admin.ModelAdmin):
    list_display = ('subject', 'name', 'view_email')

    def view_email(self, obj):
        return format_html(obj.email.email)

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.name, obj.email)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'email':
            return self.CustomModelChoiceField(queryset=Delivery.objects)
        return super(queryInfo, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Query, queryInfo)

class cartInfo(admin.ModelAdmin):
    list_display = ('user_details', 'restaurant_details', 'category_name', 'item_name', 'quantity')

    def user_details(self, obj):
        return format_html(obj.user.name + " - " + obj.user.email)

    def restaurant_details(self, obj):
        return format_html(obj.restaurant.restaurant_id + " - " + obj.restaurant.restaurant_name)

    def category_name(self, obj):
        return format_html(obj.category.category)

    def item_name(self, obj):
        return format_html(obj.item.name)

    class CustomModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            if obj in User.objects.all():
                return "%s - %s" % (obj.name, obj.email)
            elif obj in Restaurant.objects.all():
                return "%s - %s" % (obj.restaurant_id, obj.restaurant_name)
            elif obj in Category.objects.all():
                return "%s - %s - %s" % (obj.restaurant.restaurant_id, obj.restaurant.restaurant_name, obj.category)
            elif obj in Item.objects.all():
                return "%s - %s - %s - %s" % (obj.category.restaurant.restaurant_id, obj.category.restaurant.restaurant_name, obj.category.category, obj.name)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            return self.CustomModelChoiceField(queryset=User.objects)
        elif db_field.name == 'restaurant':
            return self.CustomModelChoiceField(queryset=Restaurant.objects)
        elif db_field.name == 'category':
            return self.CustomModelChoiceField(queryset=Category.objects)
        elif db_field.name == 'item':
            return self.CustomModelChoiceField(queryset=Item.objects)
        return super(cartInfo, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Cart, cartInfo)