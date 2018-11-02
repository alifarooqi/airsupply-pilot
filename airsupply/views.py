from django.shortcuts import render
from .models import Item, Order
# Create your views here.

def browse(request):
    all_items = Item.objects.all()
    context = {
        'all_items': all_items
    }
    return render(request, 'airsupply/')