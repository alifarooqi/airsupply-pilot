from django.shortcuts import render
from .models import Item, Order


def browse(request):
    all_items = Item.objects.all()
    context = {
        'all_items': all_items
    }
    return render(request, 'clinic-manager/browse.html', context)