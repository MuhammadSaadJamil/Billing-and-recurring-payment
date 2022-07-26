from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from base.models import *
from usage.utils import get_user_by_pk


def get_subscriptions(request, pk):
    user = get_user_by_pk(pk)
    if not user or user.is_admin:
        return render(request, '404_err.html', {'data': 'Buyer'})

    context = {
        'subscriptions': user.profile.get().subscriptions.all(),
        'pk': pk
    }

    return render(request, '', context)


def get_feature_usage(request, pk):
    user = get_user_by_pk(pk)
    if not user or user.is_admin:
        return render(request, '404_err.html', {'data': 'Buyer'})
    context = {
        'usage': user.usage.all()
    }
    return render(request, '', context)


class UpdateUsage(UpdateView):
    model = Usage
    fields = ['unit_used']
    success_url = ''
