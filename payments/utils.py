import stripe
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string

from base.models import Transaction, User
from background_task import background

import datetime
from dateutil import relativedelta


def setup_stripe():
    stripe.api_key = settings.STRIPE_API_KEY


@background(schedule=60)
def make_payment(domain, user_id, amount=None, customer=None, schedule_payment=False):
    user = User.objects.get(id=user_id)
    if not customer:
        customer = stripe.Customer.retrieve(user.profile.stripe_id)
    if not amount:
        amount = user.amount_due['total']
        user.reset_payment()
    print(f"Making payment of {amount}$ by {user}")
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
    user_name = str(user)
    email = user.email
    send_payment_email_invoice(domain, user_name, email, amount, schedule=5)
    if schedule_payment:
        make_payment(domain, user_id, schedule_payment=True,
                     schedule=int(get_next_schedule_time(datetime.datetime.now())))


@background(schedule=60)
def send_payment_email_invoice(current_site, user_name, email, amount):
    mail_subject = f'Payment Invoice From {current_site}'
    message = render_to_string('payment/email_invoice.html', {
        'user': user_name,
        'domain': current_site,
        'amount': amount
    })
    to_email = email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def get_next_schedule_time(date):
    next_month = date + relativedelta.relativedelta(months=1)
    return (next_month - date).total_seconds()


def schedule_payments(request, user):
    domain = get_current_site(request).domain
    date = datetime.datetime.now()
    date = date.replace(day=user.profile.billing_day.day)
    make_payment(domain, user.id, schedule=int(get_next_schedule_time(date)), schedule_payment=True)
