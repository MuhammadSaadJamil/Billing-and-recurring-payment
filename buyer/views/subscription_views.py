from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse

from base.models import *
from payments.utils import make_payment
from usage.utils import get_user_by_pk, get_object_by_id


def subscribe(request, pk):
    """
    Subscribe user to a plan
    :param request:
    :param pk:
    :return:
    """
    user = get_user_by_pk(request.user.id)
    if user.is_admin or not user.profile.payment_authorized:
        return render(request, 'error/401_err.html')

    plan = get_object_by_id(Plan, pk)
    if not plan:
        return render(request, 'error/404_err.html', {'data': 'plan'})
    profile = user.profile
    for subscription in user.profile.subscriptions.all():
        if subscription.plan and subscription.plan.id == plan.id:
            return render(request, 'error/general_err.html',
                          {'message': f'{user} Already Subscribed to the plan'})
    subscription = Subscription.objects.create(plan=plan)
    for feature in subscription.plan.features.all():
        Usage.objects.create(buyer=user, subscription=subscription, feature=feature)
    profile.subscriptions.add(subscription)
    profile.save()

    # make_payment(get_current_site(request).domain, user.id, subscription.plan.monthly_fee, schedule=5)
    make_payment.now(get_current_site(request).domain, user.id, subscription.plan.monthly_fee, make_sync=True)
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
