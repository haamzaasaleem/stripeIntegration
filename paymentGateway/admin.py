from django.contrib import admin
from paymentGateway.models import *


# Register your models here.
@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'product']
