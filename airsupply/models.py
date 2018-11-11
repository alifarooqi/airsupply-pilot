from django.db import models
from datetime import datetime

#debugging:
import logging
logger = logging.getLogger(__name__)


class Place(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=100, decimal_places=6)
    longitude = models.DecimalField(max_digits=100, decimal_places=6)
    altitude = models.IntegerField()

    def __str__(self):
        return str(self.id) + ": "+self.name


class InterPlaceDistance(models.Model):
    fromLocation = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='from_place')
    toLocation = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='to_place')
    distance = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.id) + ": "+str(self.fromLocation)+" -> "+str(self.toLocation)

    class Meta:
        unique_together = ("fromLocation", "toLocation")


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id) + ": "+self.name

    class Meta:
        verbose_name_plural = "categories"


class Item(models.Model):
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=100, decimal_places=2)
    imageUrl = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id) + ": "+self.description


class LineItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.id) + ": "+str(self.item) + " x"+str(self.quantity)


class OrderManager(models.Manager):
    def preferred_order(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        qs = qs.annotate(
            custom_order=models.Case(
                models.When(status='High', then=models.Value(0)),
                models.When(status='Medium', then=models.Value(1)),
                models.When(status='Low', then=models.Value(2)),
                default=models.Value(3),
                output_field=models.IntegerField(), )
        ).order_by('custom_order', '-timeOrdered')
        return qs


class Order(models.Model):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"
    prioList = ((HIGH, HIGH), (MEDIUM, MEDIUM), (LOW, LOW), (NONE, NONE))

    QP = "Queued for Processing"
    PW = "Processing by Warehouse"
    QD = "Queued for Dispatch"
    DIS = "Dispatched"
    DEL = "Delivered"
    CART = "Cart"
    statusList = ((QP, QP), (PW, PW), (QD, QD), (DIS, DIS), (DEL, DEL), (CART, CART))

    objects = OrderManager()

    items = models.ManyToManyField(LineItem, blank=True, null=True)
    location = models.ForeignKey(Place, on_delete=models.CASCADE, default=None)
    priority = models.CharField(max_length=100, choices=prioList)
    status = models.CharField(max_length=100, choices=statusList)
    totalWeight = models.DecimalField(max_digits=100, decimal_places=2)
    timeOrdered = models.DateTimeField(blank=True, null=True)
    timeDelivered = models.DateTimeField(blank=True, null=True)
    timeDispatched = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ": "+self.priority + " - " + str(self.location) #+ self.clinicManager.clinic_name

    def delete_order(self):
        for lt in self.items:
            lt.delete()
        self.delete()

    def update_status(self, status):
        if status == "Dispatched":
            self.timeDispatched = datetime.now()
        elif status == "Queued for Processing":
            self.timeOrdered = datetime.now()
        self.status = status
        self.save()


class CartManager(models.Manager):
    # when clinic manager logs in, create a cart. ie. when browser is reached. but right now no CM so no linking to
    # correct location. right now its linking to Mui Wo
    def create_cart(self):
        cart = self.create(priority=Order.NONE, status=Order.CART, totalWeight=0.0, location=Place.objects.get(id=4))
        cart.save()
        return cart


class Cart(Order):
    objects = CartManager()

    def __str__(self):
        return str(self.id) + ": "+str(self.items.count()) + " - " + str(self.totalWeight)

    def checkTotalWeight(self, lineitem):
        if float(self.totalWeight) + int(lineitem.quantity) * float(lineitem.item.weight) > 23.8:
            return False
        else:
            return True

    def addLineItem(self, lineitem):
        lineItems = self.items.all()
        for lt in lineItems:
            if lt.item == lineitem.item:
                lt.quantity += int(lineitem.quantity)
                lt.save(update_fields=['quantity'])
                break
        else:
            self.items.add(lineitem)
        self.totalWeight = float(self.totalWeight) + (int(lineitem.quantity) * float(lineitem.item.weight))
        self.save()

    def checkout(self, priority):
        try:
            self.priority = priority
            self.update_status("Queued for Processing")
            self.save(update_fields=['priority'])
            self.delete(keep_parents=True)
            Cart.objects.create_cart()
        except KeyError:
            return False
        else:
            return True


class DroneLoad(models.Model):
    TRUE = "TRUE"
    FALSE = "FALSE"
    statusList = ((TRUE, 'True'), (FALSE, 'False'))

    orders = models.ManyToManyField(Order, blank=True, null=True)
    dispatched = models.CharField(max_length=5, choices=statusList, default=FALSE)

    def __str__(self):
        return str(self.id) + ": "+str(self.orders.count())+" orders"

    def dispatch(self):
        all_orders = self.orders.all()
        for order in all_orders:
            #emailClinicManager
            order.update_status("Dispatched")
        self.dispatched = self.TRUE
        self.save()
