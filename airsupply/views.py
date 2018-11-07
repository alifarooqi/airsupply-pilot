from django.views import generic
from django.shortcuts import render
from django.template.defaulttags import register
from .models import Item, Category, Order, LineItem, Cart, DroneLoad
from django.http import JsonResponse
from django.urls import reverse

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
        for item in items:
            itemWeights[item] = item.item.weight * item.quantity
        context['weights'] = itemWeights
        return context


class OrderView(generic.ListView):
    template_name = 'clinic-manager/view-orders.html'
    context_object_name = 'all_orders'

    def get_queryset(self):
        return Order.objects.all()


class DispatchView(generic.ListView):
    template_name = 'dispatcher/dispatch-queue.html'
    context_object_name = 'all_droneloads'

    def get_queryset(self):
        return DroneLoad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dLs = DroneLoad.objects.all()
        dlWeights = {}
        for dl in dLs:
            sum = 0.0
            for orders in dl.orders.all():
                sum += float(orders.totalWeight)
            dlWeights[dl] = sum
        context['dlWeights'] = dlWeights
        return context


class PriorityQueueView(generic.ListView):
    template_name = 'warehouse-personnel/priority-queue.html'


def forgot_password(request):
    return render(request, 'forgot-password.html', {})


def cart_add(request):# in first iteration, no clinic manager so we get the one available cart
    try:
        item = Item.objects.get(id=request.POST['itemID'])
        quantity = request.POST['qty']
    except(KeyError, Item.DoesNotExist):
        return JsonResponse({'success': False, 'error_message': 'Item does not exist'})
    else:
        cart = Cart.objects.get(status='cart')

        newItem = LineItem()
        newItem.item = item
        newItem.quantity = quantity
        if cart.checkTotalWeight(newItem):
            newItem.save()
            cart.addLineItem(newItem)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': 'Cart weight limit exceeded'})


def cart_checkout(request):# in first iteration, no clinic manager so we get the one available cart
    priority = request.POST['priority']

    cart = Cart.objects.get(status='cart')
    if cart.checkout(priority):
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
