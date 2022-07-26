from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import User, BuyerProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, admin=False, commit=True, update=False):
        user = super().save(self)
        user.is_superuser = admin
        user.is_staff = admin
        user.user_type = user.user_type_choices[0][0] if admin else user.user_type_choices[1][0]
        if not update:
            user.is_active = admin
        user.save()
        if not admin and not update:
            BuyerProfile.objects.create(user=user)

        return user


class AccountSetupForm(SignupForm):
    email = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_img', 'password1', 'password2']

    def save(self, admin=False, commit=True, update=True):
        super(AccountSetupForm, self).save(admin, commit, update)
