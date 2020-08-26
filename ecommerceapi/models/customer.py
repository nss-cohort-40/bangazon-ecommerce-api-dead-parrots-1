from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=75)
    phone_number = models.CharField(max_length=10)

    class Meta:
        verbose_name = ("customer")
        verbose_name_plural = ("customers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})
