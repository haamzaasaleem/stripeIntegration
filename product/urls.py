from django.urls import path, include
from rest_framework import routers
from product.views import *
from paymentGateway.views import *
router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
urlpatterns = [

    path('', include(router.urls)),
    path('products/', checkout),
    path('success/', success),
    path('cancel/', cancel),
    path('create-checkout-session/<int:pk>/', CreateStripeCheckoutSession.as_view()),
    # path('success/', SuccessView.as_view(), name="success"),
    path('stripe-webhook/', StripeWebhook.as_view())
]
