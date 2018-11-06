from django.db import models


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
    status = models.CharField(max_length=100)
    totalWeight = models.DecimalField(max_digits=100, decimal_places=2)
    timeOrdered = models.DateTimeField(blank=True, null=True)
    timeDelivered = models.DateTimeField(blank=True, null=True)
    timeDispatched = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.status + " - " #+ self.clinicManager.clinic_name

    class Meta:
        ordering =['-timeOrdered']


class Cart(Order):

    def __str__(self):
        return str(self.items.count()) + " - " + str(self.totalWeight)

    def calculateTotalWeight(self):
        total = 0
        for item in self.items:
            total += item.weight
        self.totalWeight = total

    def addToTotalWeight(self, item):
        self.totalWeight += item.weight
