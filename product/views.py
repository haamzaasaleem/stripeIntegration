# from rest_framework.response import Response
from rest_framework import viewsets
from product.models import *
from product.serializers import *
from rest_framework.response import Response
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    # def list(self, request, *args, **kwargs):
    #     import pdb;pdb.set_trace()
    #     return Response(
    #         {"msg": "Request.header"}
    #     )