from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from usage.utils import get_user_by_pk


class LoginMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = get_user_by_pk(self.request.user.id)
        return user and user.is_admin


def is_admin(user):
    """
    Function based mixin for checking user type
    :param user:
    :return:
    """
    return user and user.is_admin
