
from django.db import models
from product.models import ProductModel


# Create your models here.
class TransactionModel(models.Model):
    transaction_id = models.CharField(max_length=100)
    payment_status=models.CharField(max_length=100, default='')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True, null=True)

