from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from accounts.utils import to_base64
from base.models import Plan
from usage.utils import get_user_by_pk


def index(request):
    """

    :param request:
    :return: Home view for authenticated and unauthenticated user
    """
    if request.user.is_authenticated:
        user = get_user_by_pk(request.user.id)
        if user.is_admin:
            return render(request, 'admin_templates/home.html', {'home': 'active'})
        context = {
            'home': 'active',
            'plans': Plan.objects.all(),
            'title': 'home',
            'heading': 'Subscriptions'
        }
        return render(request, 'buyer/home.html', context)
    return render(request, 'index.html')


def unauthorized(request):
    return render(request, 'error/401_err.html')


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
