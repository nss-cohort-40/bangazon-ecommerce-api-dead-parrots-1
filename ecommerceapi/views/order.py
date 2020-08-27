from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import PaymentType, Customer, Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name="orders",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'customer', 'payment_type',
          'products', 'created_at'
        )
        depth = 2



class Orders(ViewSet):
    """Orders for Bangazon customers"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer payment type
        
          Returns: JSON serialized payment type instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to orders
        
          Returns: Response JSON serialized list of order
        """
        customer = Customer.objects.get(user=request.auth.user)

        orders = Order.objects.filter(customer_id=customer.id)

        serializer = OrderSerializer(
          orders,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)
