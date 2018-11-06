from django.contrib import admin
from .models import Item, Category, Order, Cart, LineItem

admin.site.register(Item)
admin.site.register(LineItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
