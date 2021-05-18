import random, string
from django.contrib import admin
from .models import Address, Query

class addressAdminInfo(admin.ModelAdmin):
    model = Address

    def get_changeform_initial_data(self, request):
        id_list = list(Address.objects.values_list('address_id', flat=True))
        while True:
            id = ''.join(random.choice(string.ascii_letters) for x in range(5)) + str(random.randint(10000, 99999))
            if id not in id_list:
                return {'address_id': id}

admin.site.register(Address, addressAdminInfo)

admin.site.register(Query)