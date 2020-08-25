"""View module for handling request about payment types"""
from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import PaymentType, Customer


class PaymentTypeSeralizer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers
    """

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttypes',
            lookup_field='id'
        )
        fields = (
          'id', 'url', 'merchant_name', 'account_number',
          'expiration_date', 'customer_id', 'created_at'
        )
        depth = 2

class PaymentTypes(ViewSet):
    """Payment types for Bangazon customers"""

    def create(self, request):
      """Handle POST opertations

        Returns:
            Response: JSON serialzied PaymentType instance
      """

      customer = Customer.objects.get(user=request.auth.user)

      new_payment_type = PaymentType()
      new_payment_type.merchant_name = request.data["merchant_name"]
      new_payment_type.account_number = request.data["account_number"]
      new_payment_type.expiration_date = request.data["expiration_date"]
      new_payment_type.customer_id = customer.id
      new_payment_type.created_at = date.today()
      new_payment_type.save()
      
      serializer = PaymentTypeSeralizer(new_payment_type, context={'request': request})

      return Response(serializer.data)


    def destroy(self, request, pk=None):
        """Handles DELETE requests for single payment type"""

        try:
            payment = PaymentType.objects.get(pk=pk)
            payment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer payment type
        
          Returns: JSON serialized payment type instance
        """
        try:
            payment = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSeralizer(payment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to payment types
        
          Returns: Response JSON serilaized list of payment types
        """
      
        customer = Customer.objects.get(user=request.auth.user)

        payment_types = PaymentType.objects.filter(customer_id=customer.id)
    
        serializer = PaymentTypeSeralizer(
          payment_types,
          many=True,
          context={'request': request}
        )
        return Response(serializer.data)
