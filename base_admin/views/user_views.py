from django.views.generic import ListView

from base.models import User


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
