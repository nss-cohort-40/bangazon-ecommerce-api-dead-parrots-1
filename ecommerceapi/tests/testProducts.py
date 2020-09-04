import json
from rest_framework import status
from unittest import skip
from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Product, ProductType, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestProduct(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user=self.user, address='123 street', phone_number='1516516')
        self.product_type = ProductType.objects.create(name="stuff")

    def test_post_product(self):

        new_product = {
            "title": "Drill",
            "price": 100,
            "description": "drills stuff",
            "quantity": 100,
            "location": "Nashville",
            "image_path": "image.png",
            "created_at": "2020-09-03 19:38:59.746000",
            "product_type_id": self.product_type.id, 
            "local_delivery": False,
        }

        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )
          
        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one ParkArea instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Product.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Product.objects.get().title, 'Drill')
    
    def test_get_products(self):

        new_product = Product.objects.create(
          title="drill",
          price=100,
          description="drills stuff",
          quantity=100,
          location="Nashville",
          image_path="image.png",
          created_at="2020-09-03 19:38:59.746000",
          product_type_id=self.product_type.id,
          local_delivery=False,
          seller_id=1
        )

        # Now we can grab all the area (meaning the one we just created) from the db
        response = self.client.get(reverse('product-list'))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialized data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["title"], "drill")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_product.title.encode(), response.content)

    def test_delete_product(self):
        
        new_product = Product.objects.create(
          title="drill",
          price=100,
          description="drills stuff",
          quantity=100,
          location="Nashville",
          image_path="image.png",
          product_type_id=self.product_type.id,
          local_delivery=False,
          seller_id=1
        )

        response = self.client.get(reverse('product-list'))

        self.assertEqual(response.data[0]["title"], "drill")

        url = reverse('product-detail', kwargs={'pk': new_product.id})
        self.client.delete(url, HTTP_AUTHORIZATION='Token ' + str(self.token)) 

        response = self.client.get(reverse('product-list'))

        self.assertEqual(Product.objects.count(), 0)

    @skip('donno')
    def test_update_product(self):

        new_product = Product.objects.create(
          title="drill",
          price=100,
          description="drills stuff",
          quantity=100,
          location="Nashville",
          image_path="image.png",
          created_at="2020-09-03 19:38:59.746000",
          product_type_id=self.product_type.id,
          local_delivery=False,
          seller_id=1
        )

        updated_product = {
          "title":"drill",
          "price":100,
          "description":"drills stuff",
          "quantity":200,
          "location":"Nashville",
          "image_path":"image.png",
          "created_at":"2020-09-03 19:38:59.746000",
          "product_type_id":self.product_type.id,
          "local_delivery":False,
          "seller_id":1
        }
        
        response = self.client.put(reverse('product-list'),
            data=json.dumps(updated_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
