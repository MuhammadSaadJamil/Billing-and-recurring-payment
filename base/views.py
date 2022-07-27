from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from accounts.utils import to_base64
from usage.utils import get_user_by_pk


def index(request):
    """

    :param request:
    :return: Home view for authenticated and unauthenticated user
    """
    if request.user.is_authenticated:
        user = get_user_by_pk(request.user.id)
        if user.is_admin:
            return render(request, 'Admin/home.html', {'home': 'active'})
        return render(request, 'buyer/home.html', {'home': 'active'})
    return render(request, 'index.html')


def unauthorized(request):
    return render(request, 'error/401_err.html')


@login_required()
def get_profile(request):
    user = get_user_by_pk(request.user.id)
    if user.is_admin:
        context = {
            'user': user,
            'button': 'Update Profile',
            'title': 'Profile',
            'heading': 'Profile',
            'link': reverse('update-profile', args=[to_base64(user.id)]),
            'profile': 'active'
        }
        return render(request, 'Admin/profile.html', context)
