from django.db import models
from datetime import date

class OrderProduct(models.Model):

  """"Creates join table for the many to many realtionship between products and orders"""

  product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)
  order = models.ForeignKey("Order", on_delete=models.CASCADE)

  class Meta:
    verbose_name = ("order_product")
    verbose_name_plural = ("order_products")
