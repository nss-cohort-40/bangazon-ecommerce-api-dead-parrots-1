from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Order
from ..models import Customer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'products', 'payment_type_id')
        depth = 1

class Orders(ViewSet):
    def list(self, request):

        history = self.request.query_params.get('history', None)
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer_id=customer.id, payment_type_id=None)

        if history is not None:
            orders = Order.objects.filter(customer_id=customer.id)

        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)