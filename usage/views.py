from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView

from base.mixins import IsAdminMixin, LoginMixin
from base.models import *
from usage.utils import get_user_by_pk


def get_subscriptions(request, pk):
    user = get_user_by_pk(pk)
    if not user or user.is_admin:
        return render(request, 'error/404_err.html', {'data': 'Buyer'})

    context = {
        'subscriptions': user.profile.get().subscriptions.all(),
        'pk': pk
    }

    return render(request, '', context)


def get_feature_usage(request, pk):
    user = get_user_by_pk(pk)
    if not user or user.is_admin:
        return render(request, 'error/404_err.html', {'data': 'Buyer'})
    context = {
        'usage': user.usage.all(),
        'title': 'Subscription Usage',
        'heading': 'Subscription Usage',
        'usage_active': 'active'
    }
    return render(request, 'usage/usage.html', context)


class UpdateUsage(LoginMixin, IsAdminMixin, UpdateView):
    model = Usage
    fields = ['unit_used']
    template_name = 'Admin/add-form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Usage'
        context['heading'] = 'Update Usage'
        context['usage_active'] = 'active'
        context['button_text'] = 'Update Usage'
        return context

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('list-buyers')
