# from rest_framework.response import Response
from rest_framework import viewsets
from product.models import *
from product.serializers import *
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

