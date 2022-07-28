import stripe
from django.conf import settings


def setup_stripe():
    stripe.api_key = settings.STRIPE_API_KEY
