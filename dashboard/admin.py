from django.contrib import admin
from .models import Customer, Payment, Vehicle,Invoice
# Register your models here.


admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(Vehicle)
admin.site.register(Invoice)