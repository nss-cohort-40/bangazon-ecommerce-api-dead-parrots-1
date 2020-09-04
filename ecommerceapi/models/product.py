from .product_type import ProductType
from .customer import Customer
from django.db import models
from django.urls import reverse

def productFile(instance, filename):
    return '/'.join(['productimg', filename])

class Product(models.Model):

    title = models.CharField(max_length=50)
    seller = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='customers')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image_path = models.ImageField(upload_to=productFile, max_length=254, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING, related_name='products')
    local_delivery = models.BooleanField()

    class Meta:
        verbose_name = ("product")
        verbose_name_plural = ("products")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})
