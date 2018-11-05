from django.db import models


class User(models.Model):
    role = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username + " - " + self.role


class ClinicManager(User):
    clinic_name = models.CharField(max_length=100)


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


class Order(models.Model):
    items = models.ManyToManyField(Item)
    clinic_manager = models.ForeignKey(ClinicManager, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    totalWeight = models.DecimalField(max_digits=100, decimal_places=2)
    timeOrdered = models.DateTimeField(blank=True, null=True)
    timeDelivered = models.DateTimeField(blank=True, null=True)
    timeDispatched = models.DateTimeField(blank=True, null=True)

    def calculateTotalWeight(self):
        total = 0
        for item in self.items:
            total += item.weight
        self.totalWeight = total

    def addToTotalWeight(self, item):
        self.totalWeight += item.weight

    def __str__(self):
        return self.status + " - " + self.clinic_manager.clinic_name
