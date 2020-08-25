from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email',)


class Users(ViewSet):
    def retrieve(self, request, pk=None):
        '''
        Handling a GET request for a customer/user

        Returns -- JSON serialized customer instance
        '''
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''
        Handling a FETCH request for a customer/user

        Returns -- JSON serialized list of customer instances
        '''
        # user = User.objects.all()
        user = Customer.objects.filter(user=request.auth.user)

        serializer = UserSerializer(
            user, many = True, context={'request':request})

        return Response(serializer.data)


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name = 'customer',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'user', 'address', 'phone_number')
        depth = 2


class Customers(ViewSet):
    def update(self, request, pk=None):
        '''
        Handling a PUT request for a customer/user

        Returns -- Empty body with 204 status code
        '''
        customer = Customer.objects.get(pk=pk)
        customer.address = request.data['address']
        customer.phone_number = request.data['phone_number']
        customer.save()

        user = User.objects.get(pk=pk)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        # user.username = request.data['username']
        # user.email = request.data['email']
        # user.password = make_password(request.data['password'])
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        '''
        Handling a GET request for a customer/user

        Returns -- JSON serialized customer instance
        '''
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''
        Handling a FETCH request for a customer/user

        Returns -- JSON serialized list of customer instances
        '''

        # When user logs in, filter for their profile
        customer = Customer.objects.filter(user=request.auth.user)
        serializer = CustomerSerializer(customer, many=True, context={'request': request})
        return Response(serializer.data)