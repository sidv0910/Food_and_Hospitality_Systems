import datetime
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Query, Category, Item, Orders, Feedback
from Home.models import User, Restaurant, Delivery
from User.models import Address

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'view_email')

    def view_email(self, obj):
        return format_html(obj.email.restaurant_email)

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.restaurant_name, obj.restaurant_email)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'email':
            return self.CustomModelChoiceField(queryset=Restaurant.objects)
        return super(QueryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.restaurant_id, obj.restaurant_name)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'restaurant':
            return self.CustomModelChoiceField(queryset=Restaurant.objects)
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
             return "%s - %s - %s" % (obj.restaurant.restaurant_id, obj.restaurant.restaurant_name, obj.category)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return self.CustomModelChoiceField(queryset=Category.objects)
        return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'restaurant_details', 'user_details', 'total', 'delivery_boy_details', 'status', 'delivery_date_and_time')

    def restaurant_details(self, obj):
        return format_html(obj.restaurant.restaurant_id + " - " + obj.restaurant.restaurant_name)

    def user_details(self, obj):
        return format_html(obj.user.email + " - " + obj.user.name)

    def delivery_boy_details(self, obj):
        if obj.delivery == "" or obj.delivery is None:
            return format_html("Searching")
        else:
            obj1 = Delivery.objects.get(delivery_id=obj.delivery)
            return format_html(obj1.delivery_id + " - " + obj1.name)

    def status(self, obj):
        if obj.accepted:
            if obj.food_is_being_prepared:
                if obj.ready_for_delivery:
                    if obj.picked_up:
                        if obj.out_for_delivery:
                            if obj.delivered:
                                return format_html("Delivered")
                            else:
                                return format_html("Out For Delivery")
                        else:
                            return format_html("Picked Up")
                    else:
                        return format_html("Ready For Delivery")
                else:
                    return format_html("Food Being Prepared")
            else:
                return format_html("Accepted")
        else:
            return format_html("Waiting For Restaurant Confirmation")

    def delivery_date_and_time(self, obj):
        if obj.date == datetime.date(2020, 1, 1):
            return format_html("-")
        else:
            return format_html(obj.date.strftime('%A, %b %d, %Y') + " " + obj.time.strftime('%I:%M %p'))

    class RestaurantField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.restaurant_id, obj.restaurant_name)

    class UserField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.email, obj.name)

    class DeliveryField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.delivery_id, obj.name)

    class AddressField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s - %s, %s, %s, %s - %s" % (obj.user.email, obj.user.name, obj.line1, obj.line2, obj.locality, obj.city, obj.zip)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'restaurant':
            return self.RestaurantField(queryset=Restaurant.objects)
        if db_field.name == 'user':
            return self.UserField(queryset=User.objects)
        if db_field.name == 'delivery':
            return self.DeliveryField(queryset=Delivery.objects)
        if db_field.name == 'address':
            return self.AddressField(queryset=Address.objects)
        return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'food_quality', 'order_accuracy', 'packaging')

    def order_number(self, obj):
        return format_html(str(obj.order.order_number))

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s" % (str(obj.order_number))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order':
            return self.CustomModelChoiceField(queryset=Orders.objects)
        return super(FeedbackAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)