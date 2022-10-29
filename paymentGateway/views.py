import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.views import APIView

from product.views import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    return render(request, 'products.html')


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


class CreateStripeCheckoutSession(APIView):
    # @csrf_exempt
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
        return redirect(checkout_session.url, code=303)


endpoint_secret = 'whsec_c27f400dfe82bb6602156d03de12ae43e2c732bd8c7871ee09f67d7d169eaa56'


class StripeWebhook(APIView):
    def post(self, request):
        # import pdb
        # pdb.set_trace()
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            print('ValueError')
            return HttpResponse(status=400)
            # raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print('Signature Error')
            return HttpResponse(status=400)
            # raise e
            # Passed signature verification
        print(payload)
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            print("Payment was successful.")
        return HttpResponse(status=200)
