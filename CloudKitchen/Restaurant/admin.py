from django import forms
from django.contrib import admin
from .models import Query, Category, Item, Orders
from Home.models import User, Restaurant, Delivery

admin.site.register(Query)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        '_category_name',
        '_restaurant_name',
    )

    def _category_name(self, obj):
        return obj.category

    def _restaurant_name(self, obj):
        return obj.restaurant.restaurant_id + " - " + obj.restaurant.restaurant_name

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        '_restaurant_name',
        '_category_name',
        'quantity',
        'item_type',
        'price',
    )

    def _restaurant_name(self, obj):
        return obj.category.restaurant.restaurant_id + " - " + obj.category.restaurant.restaurant_name

    def _category_name(self, obj):
        return obj.category.category

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.restaurant.restaurant_id, obj.category)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return self.CustomModelChoiceField(queryset=Category.objects)
        return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):

    class RestaurantField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.restaurant_id, obj.restaurant_name)

    class UserField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.email, obj.name)

    class DeliveryField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.delivery_id, obj.name)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'restaurant':
            return self.RestaurantField(queryset=Restaurant.objects)
        if db_field.name == 'user':
            return self.UserField(queryset=User.objects)
        if db_field.name == 'delivery':
            return self.DeliveryField(queryset=Delivery.objects)
        return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)