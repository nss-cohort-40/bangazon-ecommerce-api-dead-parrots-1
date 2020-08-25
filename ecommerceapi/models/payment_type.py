from django.db import models
from .customer import Customer

class PaymentType(models.Model):

    """model for building out tables for bangazon payment types"""

    merchant_name = models.CharField(max_length=50)
    account_number = models.IntegerField()
    expiration_date = models.DateField()
    customer = models.ForeignKey(Customer, related_name=("payment_types"), on_delete=models.DO_NOTHING)
    created_at = models.DateField()

    class Meta:
        verbose_name = ("payment_type")
        verbose_name_plural = ("payment_types")


    def __str__(self):
        return self.merchant_name, self.account_number
