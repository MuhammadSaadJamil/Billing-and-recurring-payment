from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from accounts.utils import to_base64
from base.models import *
from usage.utils import get_user_by_pk


def index(request):
    """

    :param request:
    :return: Home view for authenticated and unauthenticated user
    """
    if request.user.is_authenticated:
        user = get_user_by_pk(request.user.id)
        if user.is_admin:
            transactions = Transaction.objects.all()
            context = {
                'home': 'active',
                'plans': Plan.objects.all().count(),
                'features': Feature.objects.all().count(),
                'subscriptions': Subscription.objects.all().count(),
                'buyers': User.objects.get_buyers().count(),
                'transactions': transactions.count(),
                'data': [[str(transaction.created_at), transaction.amount_captured] for transaction in transactions],
                'title': 'home',
                'heading': 'Stats'
            }
            return render(request, 'admin_templates/home.html', context)
        context = {
            'home': 'active',
            'plans': Plan.objects.all(),
            'title': 'home',
            'heading': 'Subscriptions'
        }
        return render(request, 'buyer/home.html', context)
    return render(request, 'index.html')


def unauthorized(request):
    """
    401 Error view
    :param request:
    :return:
    """
    return render(request, 'error/401_err.html')


def card_error(request):
    return render(request, 'error/general_err.html', {'message': 'Payment Declined!'})


@login_required()
def get_profile(request):
    user = get_user_by_pk(request.user.id)
    if user:
        context = {
            'user': user,
            'button': 'Update Profile',
            'title': 'Profile',
            'heading': 'Profile',
            'link': reverse('update-profile', args=[to_base64(user.id)]),
            'profile': 'active'
        }
        return render(request, 'accounts/profile.html', context)
