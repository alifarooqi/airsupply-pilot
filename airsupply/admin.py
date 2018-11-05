from django.contrib import admin
from .models import Item, Category, Order, User, ClinicManager

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(ClinicManager)
