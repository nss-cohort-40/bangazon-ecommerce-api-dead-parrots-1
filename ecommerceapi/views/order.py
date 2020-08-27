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



    def update(self, request, pk=None):

        customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.get(pk=pk)
        payment_type = request.data["payment_type"]
        created_at = order.created_at
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    # def patch(self, request, pk=None):

    #     customer = Customer.objects.get(user=request.auth.user)
    #     try:
    #       order = Order.objects.get(pk=pk)
    #       serializer = OrderSerializer(order, data=request.data, partial=True)
    #       if serializer.is_valid():
    #           serializer.save()
    #           return Response({}, status=status.HTTP_204_NO_CONTENT)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)


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
