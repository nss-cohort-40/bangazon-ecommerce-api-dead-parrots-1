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
        fields = ('id', 'title', 'seller', 'price', 'description', 'quantity',
                  'location', 'image_path', 'created_at', 'product_type', 'local_delivery')
        depth = 2


class Products(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        newsell = Product()
        product_type = ProductType.objects.get(
            pk=request.data["product_type_id"])
        seller = Customer.objects.get(user_id=request.user.id)
        file = request.data["image_path"]

        newsell.product_type = product_type
        newsell.title = request.data["title"]
        newsell.seller = seller
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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
