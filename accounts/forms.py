from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import User, BuyerProfile


class SignupForm(UserCreationForm):
    user_choices = [('Buyer', "Buyer"), ('admin_templates', 'admin_templates')]
    email = forms.EmailField(max_length=200, help_text='Required')
    type = forms.ChoiceField(choices=user_choices, initial=user_choices[0][0])

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, admin=False, commit=True, update=False):
        if self.cleaned_data.get('type') == 'admin_templates' or admin:
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


class AccountSetupForm(SignupForm):
    email = None
    type = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_img', 'password1', 'password2']

    def save(self, admin=False, commit=True, update=True):
        super(AccountSetupForm, self).save(self.instance.is_admin, commit, update)
