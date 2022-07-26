from django.shortcuts import render

from base.models import *
from usage.utils import get_user_by_pk, get_object_by_id


def subscribe(request, pk):
    """
    Subscribe user to a plan
    :param request:
    :param pk:
    :return:
    """
    user: User = get_user_by_pk(request.user.id)
    if user.is_admin:
        return render(request, '401_err.html')
    plan = get_object_by_id(Plan, pk)
    if not plan:
        return render(request, '404_err.html', {'data': 'plan'})
    profile = user.profile
    profile.subscriptions.add(plan)
    profile.save()

    return render(request, '')


def unsubscribe(request, pk):
    """
    UnSubscribe user from a plan
    :param request:
    :param pk:
    :return:
    """
    user: User = get_user_by_pk(request.user.id)
    if user.is_admin:
        return render(request, '401_err.html')
    plan = get_object_by_id(Plan, pk)
    if not plan:
        return render(request, '404_err.html', {'data': 'plan'})
    profile = user.profile
    profile.subscriptions.remove(plan)
    profile.save()

    return render(request, '')
