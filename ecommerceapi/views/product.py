from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ecommerceapi.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    """
    class Meta: 
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id','title', 'customer_id', 'price', 'description', 'quantity', 'location', 'image_path', 'created_at')
        depth = 1

class Products(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        # order = self.request.query_params.get('order_by', None) # 'created_date'
        # direction = self.request.query_params.get('direction', None) # 'desc'
        search = self.request.query_params.get('search', None)
        products = Product.objects.all()

        if search is not None:
            products = products.filter(title=search)

        serializer = ProductSerializer(
            products, 
            many=True,
            context={'request': request}
        )
    
        return Response(serializer.data)
    


