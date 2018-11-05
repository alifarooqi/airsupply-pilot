from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)


class Item(models.Model):
    description = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=100, decimal_places=2)
    image = models.CharField(max_length=250)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    status = models.CharField(max_length=100)
    totalWeight = models.DecimalField(max_digits=100, decimal_places=2)
    timeOrdered = models.DateTimeField()
    timeDelivered = models.DateTimeField()
    timeDispatched = models.DateTimeField()
