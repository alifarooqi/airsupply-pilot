from django.db import models
from datetime import datetime


class Place(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=100, decimal_places=2)
    longitude = models.DecimalField(max_digits=100, decimal_places=2)
    altitude = models.DecimalField(max_digits=100, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Item(models.Model):
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=100, decimal_places=2)
    imageUrl = models.CharField(max_length=250)

    def __str__(self):
        return self.description


class LineItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.item) + " x"+str(self.quantity)


class Order(models.Model):
    items = models.ManyToManyField(LineItem, blank=True, null=True)
    #clinicManager = models.ForeignKey(UserForm, on_delete=models.CASCADE)
    priority = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    totalWeight = models.DecimalField(max_digits=100, decimal_places=2)
    timeOrdered = models.DateTimeField(blank=True, null=True)
    timeDelivered = models.DateTimeField(blank=True, null=True)
    timeDispatched = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.priority + " - " + self.status #+ self.clinicManager.clinic_name

    class Meta:
        ordering =['-timeOrdered']

    def delete_order(self):
        for lt in self.items:
            lt.delete()
        self.delete()


class CartManager(models.Manager):
    # when clinic manager logs in, create a cart
    def create_cart(self):
        cart = self.create(priority='none', status='cart', totalWeight=0.0)
        return cart


class Cart(Order):
    objects = CartManager()

    def __str__(self):
        return str(self.items.count()) + " - " + str(self.totalWeight)

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
                break
        else:
            self.items.add(lineitem)
        self.totalWeight = float(self.totalWeight) + (int(lineitem.quantity) * float(lineitem.item.weight))
        self.save()

    def checkout(self, priority):
        try:
            self.priority = priority
            self.status = 'Queued for Processing'
            self.timeOrdered = datetime.now()
            self.save(update_fields=['priority', 'status', 'timeOrdered'])
            self.delete(keep_parents=True)
            Cart.objects.create_cart()
        except KeyError:
            return False
        else:
            return True
