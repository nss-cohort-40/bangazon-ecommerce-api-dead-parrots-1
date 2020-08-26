from django.db import models
from django.urls import reverse

class ProductType(models.Model):

    name = models.CharField(max_length=55)

    class Meta:
        verbose_name = ("productType")
        verbose_name_plural = ("productTypes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProductType_detail", kwargs={"pk": self.pk})
