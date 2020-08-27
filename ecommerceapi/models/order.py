from django.db import models
from datetime import date
from .customer import Customer
from .payment_type import PaymentType

class Order(models.Model):

    """model for building out tables for bangazon orders"""
    customer = models.ForeignKey(Customer, related_name=("customer_order"), on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(PaymentType, related_name=("payment_type"), on_delete=models.DO_NOTHING, null=True, blank=True)
    products = models.ManyToManyField("Product", through=("OrderProduct"))
    created_at = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")


    def __str__(self):
        return self.customer, self.payment_type
