from django.db import models
from django.utils import timezone

# Create your models here.


class Customer(models.Model):
    name = models.CharField()
    email = models.EmailField(unique=True)
    phone = models.CharField(null=True, blank=True)


class Product(models.Model):
    name = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField(default=0)


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_ids = models.ManyToManyField(Product)
    order_date = models.DateTimeField(default=timezone.now)
