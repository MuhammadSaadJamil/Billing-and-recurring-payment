from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from base.models import User
from payments.utils import schedule_payments
from usage.utils import get_user_by_pk


class ListBuyers(ListView):
    template_name = 'admin_templates/list-buyer.html'
    model = User
    queryset = User.objects.get_buyers()
    context_object_name = 'buyers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Buyers List'
        context['heading'] = 'Select Buyer'
        context['usage_active'] = 'active'
        return context


def toggle_charge_buyer(request, pk):
    user = get_user_by_pk(pk)
    if not user or user.is_admin:
        return render(request, 'error/404_err.html', {'data': 'buyer'})
    if user.profile.charge_on_billing_day:
        return render(request, 'error/general_err.html', {'message': 'already charging user'})
    profile = user.profile
    profile.charge_on_billing_day = not profile.charge_on_billing_day
    schedule_payments(request, user)
    profile.save()
    return redirect(reverse('list-buyers'))
