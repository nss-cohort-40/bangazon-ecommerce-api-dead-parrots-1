from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import OrderProduct
from ..models import Customer
from ..models import Order
from ..models import Product
from .order import OrderSerializer

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    
    # order = OrderSerializer()

    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'product_id')
        depth = 2

class OrderProducts(ViewSet):

    def create(self, request):
        customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.get(customer_id=customer.id, payment_type_id=None)
        product = Product.objects.get(pk=request.data["product_id"])
        product.quantity -= 1
        product.save()
        neworder_product = OrderProduct()
        neworder_product.order_id = order.id
        neworder_product.product_id = product.id

        neworder_product.save()

        serializer = OrderProductSerializer(neworder_product, context={'request': request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):

        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.get(customer_id=customer.id, payment_type_id=None)

        order_products = OrderProduct.objects.filter(order_id=order.id)

        serializer = OrderProductSerializer(
            order_products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
