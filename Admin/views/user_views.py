from django.views.generic import ListView

from base.models import User


class ListBuyers(ListView):
    model = User
    queryset = User.objects.get_buyers()
    context_object_name = 'buyers'
