from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import *
from base.models import *


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
            message = render_to_string('acc_active_email.html', {
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
            return HttpResponse('Please confirm your email address to complete the registration')
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
            return HttpResponse('Account already activated!')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, User.MultipleObjectsReturned):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(f'Thank you for your email confirmation. Now you can login your account.<br>'
                            f'visit <a href="{reverse("update-profile", args=[uidb64])}">Here</a>')
    else:
        return HttpResponse('Activation link is invalid!')


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
        return render(request, '404_err.html', {'data': 'User'})

    if request.POST:
        form = AccountSetupForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    form = AccountSetupForm(instance=user)
    data = {
        'form': form
    }
    return render(request, 'signup.html', data)


class Login(LoginView):
    """
    Login view
    """
    template_name = 'signup.html'  # change later
    redirect_authenticated_user = True
    next_page = reverse_lazy('update-profile', args=['hmmm'])


class Logout(LogoutView):
    """
    Logout view
    """
    next_page = reverse_lazy('signup')
