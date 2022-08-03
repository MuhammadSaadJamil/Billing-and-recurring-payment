from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from base.models import User, BuyerProfile
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation


class SignupForm(UserCreationForm):
    user_choices = [('Buyer', "Buyer"), ('Admin', 'Admin')]
    email = forms.EmailField(max_length=200, help_text='Required')
    type = forms.ChoiceField(choices=user_choices, initial=user_choices[0][0])

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, admin=False, commit=True, update=False):
        if self.cleaned_data.get('type') == 'Admin' or admin:
            is_admin = True
        else:
            is_admin = False
        user = super().save(self)
        user.is_superuser = is_admin
        user.is_staff = is_admin
        user.user_type = user.user_type_choices[0][0] if is_admin else user.user_type_choices[1][0]
        if not update:
            user.is_active = is_admin
        user.save()
        if not is_admin and not update:
            BuyerProfile.objects.create(user=user)

        return user


class AccountSetupForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_img', 'password1', 'password2']

    def save(self, admin=False, commit=True, update=True):
        if self.cleaned_data.get('first_name'):
            self.instance.first_name = self.cleaned_data.get('first_name')
        if self.cleaned_data.get('last_name'):
            self.instance.last_name = self.cleaned_data.get('last_name')
        if self.cleaned_data.get('profile_img'):
            self.instance.profile_img = self.cleaned_data.get('profile_img')
        if self.cleaned_data.get('password2'):
            self.instance.set_password(self.cleaned_data.get('password2'))
        self.instance.save()
        return self.instance
