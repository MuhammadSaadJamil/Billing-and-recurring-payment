import stripe
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from base.models import Transaction, User


def setup_stripe():
    stripe.api_key = settings.STRIPE_API_KEY


def make_payment(request, user, amount, customer=None):
    if not customer:
        customer = stripe.Customer.retrieve(user.profile.stripe_id)
    charge = stripe.Charge.create(
        customer=customer,
        amount=amount * 100,
        currency='usd',
        description="Subscriptions"
    )
    profile = user.profile
    transaction = Transaction.objects.create(
        brand=charge.payment_method_details.card.brand,
        last4=charge.payment_method_details.card.last4,
        transaction_id=charge.id,
        amount_captured=charge.amount_captured
    )
    profile.transactions.add(transaction)
    profile.save()
    send_payment_email_invoice(request, user, amount)


def send_payment_email_invoice(request, user, amount):
    current_site = get_current_site(request)
    mail_subject = f'Payment Invoice From {current_site.domain}'
    message = render_to_string('payment/email_invoice.html', {
        'user': user,
        'domain': current_site.domain,
        'amount': amount
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
