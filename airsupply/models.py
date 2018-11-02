from django.db import models


class Item(models.Model):

    description = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    weight = models.DecimalField()
    image = models.CharField(max_length=250)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    status = models.CharField(max_length=100)
    totalWeight = models.DecimalField()
    timeOrdered = models.DateTimeField()
    timeDelivered = models.DateTimeField()
    timeDispatched = models.DateTimeField()
