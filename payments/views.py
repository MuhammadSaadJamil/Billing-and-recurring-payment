import stripe
from django.shortcuts import render

from base.models import User, Transaction
from payments.utils import setup_stripe
from usage.utils import get_user_by_pk

setup_stripe()


def authorize_payment(request):
    if request.POST:
        if request.user.is_authenticated:
            user = get_user_by_pk(request.user.id)
            if user.is_buyer:
                if not user.profile.payment_authorized:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=user.get_full_name(),
                        source=request.POST['stripeToken']
                    )
                    profile = user.profile
                    profile.stripe_token = request.POST.get('stripeToken')
                    profile.stripe_id = customer.id
                    profile.save()

                    make_payment(user, customer, 5)
                else:
                    customer = stripe.Customer.retrieve(user.profile.stripe_id)
                    make_payment(user, customer, 10)
    return render(request, 'payment/authorize.html')


def make_payment(user: User, customer, amount):
    charge = stripe.Charge.create(
        customer=customer,
        amount=amount * 100,
        currency='usd',
        description="Donation"
    )
    print(charge)
    profile = user.profile
    transaction = Transaction.objects.create(
        brand=charge.payment_method_details.card.brand,
        last4=charge.payment_method_details.card.last4,
        transaction_id=charge.id,
        amount_captured=charge.amount_captured
    )
    profile.transactions.add(transaction)
    profile.save()
