from django.contrib import admin
from .models import Item, Category, Order, Cart, LineItem, Place, InterPlaceDistance, DroneLoad

admin.site.register(Place)
admin.site.register(InterPlaceDistance)
admin.site.register(Item)
admin.site.register(LineItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(DroneLoad)
