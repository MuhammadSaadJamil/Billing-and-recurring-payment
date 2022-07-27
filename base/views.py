from django.shortcuts import render

from usage.utils import get_user_by_pk


def index(request):
    """

    :param request:
    :return: Home view for authenticated and unauthenticated user
    """
    if request.user.is_authenticated:
        user = get_user_by_pk(request.user.id)
        if user.is_admin:
            return render(request, 'Admin/home.html')
        return render(request, 'buyer/home.html')
    return render(request, 'index.html')


def unauthorized(request):
    return render(request, 'error/401_err.html')
