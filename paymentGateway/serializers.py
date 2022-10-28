from rest_framework import serializers
from paymentGateway.models import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'
