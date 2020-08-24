from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ecommerceapi.models import Product, ProductType

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
            product = Products.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        newsell = Product()
        product_type = ProductType.objects.get(pk=request.data["producttype_id"])

        newsell.product_type = product_type
        newsell.title = request.data["title"]
        newsell.customer_id = request.data["customer_id"]
        newsell.price = request.data["price"]
        newsell.description = request.data["description"]
        newsell.quantity = request.data["quantity"]
        newsell.location = request.data["location"]
        newsell.image_path = request.data["image_path"]
        newsell.created_at = request.data["created_at"]
        newsell.save()

        serializer = ProductSerializer(newsell, context={'request': request})

        return Response(serializer.data)
        

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    