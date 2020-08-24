from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.urls import reverse

class Product(models.Model):

    title = models.CharField(max_length=50)
    customer_id = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=50)
    quantity = models.IntegerField()
    location = models.CharField(max_length=50)
    image_path = models.CharField(max_length=50)
    created_at = models.DateTimeField()


    class Meta:
        verbose_name = ("product")
        verbose_name_plural = ("products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})
