from django.contrib import admin

from base.models import Category, Customer, Medicine, Order, OrderItem, Prescription, Covid

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Category)

admin.site.register(Medicine)
admin.site.register(Covid)
admin.site.register(Prescription)
admin.site.register(OrderItem)
