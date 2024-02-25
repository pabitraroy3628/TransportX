from django.contrib import admin

# Register your models here.
from .models import Customer, Book, Order, Request_Book, Shipment

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Request_Book)
admin.site.register(Shipment)