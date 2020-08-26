from django.http import HttpResponseServerError 
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from rest_framework import serializers, status
from ecommerceapi.models import Product, ProductType, Customer

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    """
    class Meta: 
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id','title', 'customer', 'price', 'description', 'quantity', 'location', 'image_path', 'created_at', 'product_type', 'local_delivery')
        depth = 2

class Products(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        newsell = Product()
        product_type = ProductType.objects.get(pk=request.data["product_type_id"])
        customer = Customer.objects.get(pk=request.data["customer_id"])
        file = request.data["image_path"]

        newsell.product_type = product_type
        newsell.title = request.data["title"]
        newsell.customer = customer
        newsell.price = request.data["price"]
        newsell.description = request.data["description"]
        newsell.quantity = request.data["quantity"]
        newsell.location = request.data["location"]
        newsell.image_path = file
        newsell.created_at = request.data["created_at"]
        newsell.local_delivery = request.data["local_delivery"]
        newsell.save()

        serializer = ProductSerializer(newsell, context={'request': request})

        return Response(serializer.data)
        


    def list(self, request):
        search = self.request.query_params.get('search', None)
        quantity = self.request.query_params.get('quantity', None)
        products = Product.objects.all()

        if quantity is not None:
            try:
                products = products.order_by("created_at")[:int(quantity)]
            except ValueError:
                products = products.objects.all()
        if search is not None:
            products = products.filter(title=search)

        serializer = ProductSerializer(
            products, 
            many=True,
            context={'request': request}
        )
        
        return Response(serializer.data)
