import random, string
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Address, Query
from Home.models import User

class addressAdminInfo(admin.ModelAdmin):
    model = Address

    list_display = ('address_id', 'user_details', 'complete_address', 'landmark')

    def user_details(self, obj):
        return format_html(obj.user.name + " - " + obj.user.email)

    def complete_address(self, obj):
        return format_html(obj.line1 + ", " + obj.line2 + ", " + obj.locality + ", " + obj.city + " - " + str(obj.zip))

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.name, obj.email)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            return self.CustomModelChoiceField(queryset=User.objects)
        return super(addressAdminInfo, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        id_list = list(Address.objects.values_list('address_id', flat=True))
        while True:
            id = ''.join(random.choice(string.ascii_letters) for x in range(5)) + str(random.randint(10000, 99999))
            if id not in id_list:
                return {'address_id': id}

admin.site.register(Address, addressAdminInfo)

class queryInfo(admin.ModelAdmin):
    list_display = ('subject', 'name', 'view_email')

    def view_email(self, obj):
        return format_html(obj.email.email)

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s - %s" % (obj.name, obj.email)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'email':
            return self.CustomModelChoiceField(queryset=User.objects)
        return super(queryInfo, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Query, queryInfo)