from django.shortcuts import render, redirect
from django.urls import reverse

from base.models import *
from usage.utils import get_user_by_pk, get_object_by_id


def subscribe(request, pk):
    """
    Subscribe user to a plan
    :param request:
    :param pk:
    :return:
    """
    user = get_user_by_pk(request.user.id)
    if user.is_admin:
        return render(request, 'error/401_err.html')
    plan = get_object_by_id(Plan, pk)
    if not plan:
        return render(request, 'error/404_err.html', {'data': 'plan'})
    profile = user.profile
    subscription = Subscription.objects.create(plan=plan)
    profile.subscriptions.add(subscription)
    profile.save()

    return redirect(reverse('home'))


def unsubscribe(request, pk):
    """
    UnSubscribe user from a plan
    :param request:
    :param pk:
    :return:
    """
    user: User = get_user_by_pk(request.user.id)
    if user.is_admin:
        return render(request, 'error/401_err.html')
    subscription = get_object_by_id(Subscription, pk)
    if not subscription:
        return render(request, 'error/404_err.html', {'data': 'Subscription'})
    profile = user.profile
    profile.subscriptions.remove(subscription)
    profile.save()
    subscription.delete()

    return render(request, '')
