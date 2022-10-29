import json

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.views import APIView
from paymentGateway.models import TransactionModel
from product.models import ProductModel
from paymentGateway.serializers import TransactionSerializer
from django.views.decorators.csrf import csrf_exempt


from product.views import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    return render(request, 'products.html')


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


class CreateStripeCheckoutSession(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        DOMAIN = 'http://127.0.0.1:8000/api/'

        prod_id = self.kwargs['pk']
        product = ProductModel.objects.get(id=prod_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': '{{PRICE_ID}}',
                    # 'quantity': 1,
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.name

                        }
                    },
                    'quantity': 1,
                },

            ],
            mode='payment',
            metadata={
                'product_id': product.id
            },
            success_url=DOMAIN + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=DOMAIN + 'cancel/',

        )
        context = {
            'session_id': checkout_session.id,
            'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
        }
        return redirect(checkout_session.url, code=303)


endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class StripeWebhook(APIView):

    def post(self, request):
        print('webhook!')
        # import pdb;pdb.set_trace()
        event = None
        payload = request.body

        if endpoint_secret:
            # print(request.headers['Stripe-Signature'])
            sig_header = request.headers.get('stripe-signature')
            # print(sig_header)
            try:
                event = stripe.Webhook.construct_event(
                    payload=payload, sig_header=sig_header, secret=endpoint_secret
                )
                # print(event)
            except stripe.error.SignatureVerificationError as e:
                print('⚠️  Webhook signature verification failed.' + str(e))
                return HttpResponse(status=400)
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                transaction_details = {
                    'transaction_id': session.payment_intent,
                    'product': session.metadata['product_id'],
                    'payment_status': session.payment_status
                }
                serializer = TransactionSerializer(data=transaction_details)
                if serializer.is_valid():
                    serializer.save()
                    # print(session.payment_intent)
                    # print(session.metadata['product_id'])
                    return HttpResponse(status=200)

            return HttpResponse(status=200)
