"""bangazonllc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from ecommerceapi.models import *
from ecommerceapi.views import Products
from ecommerceapi.views import ProductTypes
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from ecommerceapi.views import register_user
from ecommerceapi.views import login_user
from ecommerceapi.views import Customers
from ecommerceapi.views import Users
from ecommerceapi.views import PaymentTypes


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', Products, 'product')
router.register(r'paymenttypes', PaymentTypes, 'paymenttype')
router.register(r'customers', Customers, 'customers')
router.register(r'users', Users, 'user')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', register_user),
    path('login/', login_user),
]
