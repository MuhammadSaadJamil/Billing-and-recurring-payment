import stripe
from django.shortcuts import render, redirect
from django.urls import reverse

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
                    try:
                        customer = stripe.Customer.create(
                            email=user.email,
                            name=user.get_full_name(),
                            source=request.POST['stripeToken']
                        )
                        profile = user.profile
                        profile.stripe_token = request.POST.get('stripeToken')
                        profile.stripe_id = customer.id
                        profile.save()
                    except stripe.error.CardError:
                        return render(request, 'error/general_err.html', {'message': 'Card Declined.'})
                return redirect(reverse('profile'))
    context = {
        'title': 'authorize payment',
        'heading': 'Authorize Payments'
    }
    return render(request, 'payment/authorize.html', context)
