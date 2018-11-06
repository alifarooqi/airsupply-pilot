from django.views import generic
from django.shortcuts import render
from django.template.defaulttags import register
from .models import Item, Category, Order, LineItem, Cart
from django.http import JsonResponse

from django.http import HttpResponse

#debugging:
import logging
logger = logging.getLogger(__name__)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class BrowseView(generic.ListView):
    template_name = 'clinic-manager/browse.html'
    context_object_name = 'all_items'

    def get_queryset(self):
        return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = Category.objects.all()
        context['categories'] = cats
        catSizes = {}
        for cat in cats:
            catSizes[cat] = Item.objects.filter(category=cat).count()
        context['catSizes'] = catSizes
        return context


class CartView(generic.ListView):
    template_name = 'clinic-manager/cart.html'
    context_object_name = 'all_items'

    def get_queryset(self):
        return Order.objects.get(status='cart').items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Order.objects.get(status='cart').items.all()
        itemWeights = {}
        curWeight = 0
        for item in items:
            itemWeights[item] = item.weight + curWeight
            curWeight += item.weight
        context['runningTotal'] = itemWeights
        return context


class OrderView(generic.ListView):
    template_name = 'clinic-manager/view-orders.html'
    context_object_name = 'all_orders'

    def get_queryset(self):
        return Order.objects.all()


class DispatchView(generic.ListView):
    template_name = 'dispatcher/dispatch-queue.html'


class PriorityQueueView(generic.ListView):
    template_name = 'warehouse-personnel/priority-queue.html'


def forgot_password(request):
    return render(request, 'forgot-password.html', {})


def cart_add(request):# in first iteration, no clinic manager so we get the one available cart
    try:
        item = Item.objects.get(id=request.POST['itemID'])
        quantity = request.POST['qty']
    except(KeyError, Item.DoesNotExist):
        return HttpResponse("error")
    else:
        newItem = LineItem.objects.create(item=item, quantity=quantity)
        cart = Cart.objects.get(status='cart')
        cart.items.add(newItem)
        return JsonResponse({'success': True})



