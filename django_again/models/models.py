from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

class Mouse(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    price = models.IntegerField()
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return self.name