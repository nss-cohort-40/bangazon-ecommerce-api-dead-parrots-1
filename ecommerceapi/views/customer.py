"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer

class CustomerSeralizer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers
    """

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = (
          'id', 'url', 'user_id', 'address',
          'phone_number'
        )
        depth = 2

class Customers(ViewSet):
    """Payment types for Bangazon customers"""

    # def create(self, request):
    #   """Handle POST opertations

    #     Returns:
    #         Response: JSON serialzied PaymentType instance
    #   """

    #   new_payment_type = PaymentType()
    #   new_payment_type.merchant_name = request.data["merchant name"]
    #   new_payment_type.acc


    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer payment type
        
          Returns: JSON serialized payment type instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSeralizer(Customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to payment types
        
          Returns: Response JSON seilaized list of payment types
        """

        customers = Customer.objects.all()
        serializer = CustomerSeralizer(
          customers,
          many=True,
          context={'request': request}
        )
        return Response(serializer.data)
