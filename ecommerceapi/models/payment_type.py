# from django.db import models

# class PaymentType(models.Model):

#     """model for building out tables for bangazon payment types"""

#     merchant_name = models.CharField(max_length=50)
#     account_number = models.IntegerField()
#     expirtation_date = models.DateField()
#     customer_id = models.ForeignKey(Customer, related_name=("customers"), on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField()

#     class Meta:
#         verbose_name = ("payment type")
#         verbose_plural_name = ("payment types")


#     def __str__(self):
#         return self.merchant_name, self.account_number
