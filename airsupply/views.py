from django.views import generic
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from .models import Item, Category, Order, LineItem, Cart, DroneLoad, Place
from django.http import JsonResponse
import csv
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

    if len(Cart.objects.all()) == 0: #not identifying with user for now
        Cart.objects.create_cart()

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
        return Cart.objects.get(status=Order.CART).items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Order.objects.get(status=Order.CART).items.all()
        itemWeights = {}
        sum = 0
        for item in items:
            itemWeights[item] = item.item.weight * item.quantity
            sum += itemWeights[item]
        context['weights'] = itemWeights
        context['totalWeight'] = sum
        context['ordered'] = "FALSE"
        return context


def cart_add(request):# in first iteration, no clinic manager so we get the one available cart

    try:
        itemID = request.GET.get('itemid', 0)

        item = Item.objects.get(pk=itemID)
        quantity = request.GET.get('qty', 0)

    except(KeyError, Item.DoesNotExist):
        return JsonResponse({'success': False, 'error_message': 'Item does not exist'})
    else:
        cart = Cart.objects.get(status=Order.CART) # get any cart

        newItem = LineItem()
        newItem.item = item
        newItem.quantity = quantity
        if cart.checkTotalWeight(newItem):
            newItem.save()
            cart.addLineItem(newItem)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': 'Cart weight limit exceeded'})


class OrderView(generic.ListView):
    template_name = 'clinic-manager/view-orders.html'
    context_object_name = 'all_orders'

    def get_queryset(self):
        return Order.objects.exclude(status=Order.CART)


def cart_checkout(request):# in first iteration, no clinic manager so we get the one available cart
    priority = request.POST['priority']

    cart = Cart.objects.get(status=Order.CART)
    if cart.checkout(priority):
        return redirect('airsupply:my_orders')
    else:
        return JsonResponse({'success': False})


class OrderDetailView(generic.ListView):
    template_name = 'clinic-manager/cart.html'
    context_object_name = 'all_items'

    def get_queryset(self):
        return Order.objects.get(id=self.kwargs.get('pk')).items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs.get('pk'))
        items = order.items.all()
        itemWeights = {}
        sum = 0
        for item in items:
            itemWeights[item] = item.item.weight * item.quantity
            sum += itemWeights[item]
        context['weights'] = itemWeights
        context['totalWeight'] = sum
        context['ordered'] = "TRUE"
        context['priority'] = order.priority

        return context


class DispatchView(generic.ListView):
    template_name = 'dispatcher/dispatch-queue.html'
    context_object_name = 'all_droneloads'

    def get_queryset(self):
        return DroneLoad.objects.exclude(dispatched='TRUE')

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


def get_itinerary(request, pk):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="itinerary_005.csv"'
    writer = csv.writer(response)
    writer.writerow(['22.266040', '113.997882', '17'])
    writer.writerow(['22.265040', '113.927482', '5'])
    writer.writerow(['22.236040', '113.947882', '1'])
    writer.writerow(['22.265040', '113.995182', '10'])
    writer.writerow(['22.170257', '114.131376', '161'])





    return response


def dispatch(request, pk):
    dl = DroneLoad.objects.get(pk=pk)
    dl.dispatch()
    return redirect('airsupply:dispatch_view')


class PriorityQueueView(generic.ListView):
    template_name = 'warehouse-personnel/priority-queue.html'


def forgot_password(request):
    return render(request, 'forgot-password.html', {})

