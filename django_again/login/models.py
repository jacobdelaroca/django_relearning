from django.db import models
from django.contrib.auth.models import User


class ItemName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class ItemCondition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    quantity = models.IntegerField()
    notes = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(ItemName, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(ItemCondition, on_delete=models.SET_NULL, null=True)



