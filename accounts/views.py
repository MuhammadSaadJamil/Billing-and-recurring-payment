from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from accounts.forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from accounts.utils import *
from base.mixins import is_admin
from base.models import *
from usage.utils import get_user_by_pk


@login_required()
@user_passes_test(is_admin, login_url='/unauthorized')
def signup(request):
    """
    Signup view for creating new user by Admin. After a user is created an email is sent on his email address for
    verification and account activation
    :param request: Http request
    :return: render template
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = f'Activation link from {current_site.domain}'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': to_base64(user.id),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/confirm_email.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    """
    Account activation view that verifies a user and activate relevant account, based on link emailed to user
    :param request: Http request
    :param uidb64: user id base64 encoded
    :param token: token for user verification
    :return:
    """
    try:
        uid = decode_base64(uidb64)
        user = User.objects.get(id=uid)
        if user.is_active:
            return render(request, 'accounts/used_link.html')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, User.MultipleObjectsReturned):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/valid_link.html', {'uidb64': uidb64})
    else:
        return render(request, 'accounts/invalid_link.html')


@login_required()
def update_profile(request, uidb64):
    """
    User profile completion and edit view
    :param request: http request
    :param uidb64: user id base64 encoded
    :return:
    """
    try:
        user_id = decode_base64(uidb64)
        user = User.objects.get(id=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, User.MultipleObjectsReturned):
        user = None
    if not user:
        return render(request, 'error/404_err.html', {'data': 'User'})

    if request.POST:
        form = AccountSetupForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    form = AccountSetupForm(instance=user)
    data = {
        'form': form
    }
    return render(request, 'signup.html', data)


class Login(LoginView):
    """
    Login view
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.POST.get('username'))
        except(User.DoesNotExist, User.MultipleObjectsReturned, TypeError, ValueError, OverflowError):
            user = None
        if user and not user.is_active:
            return render(request, 'accounts/not_active.html')
        return super().post(request, *args, **kwargs)


class Logout(LogoutView):
    """
    Logout view
    """
    next_page = reverse_lazy('login')
