from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers import UserManager


class User(AbstractUser):
    user_type_choices = [('A', 'Admin'), ('B', 'buyer')]
    user_type = models.CharField(max_length=1, null=False, blank=False, default=user_type_choices[0],
                                 choices=user_type_choices)
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    profile_img = models.ImageField(upload_to='Images/Profile/', null=True, blank=True)
    objects = UserManager()

    @property
    def is_admin(self):
        return self.user_type == 'A'

    @property
    def is_buyer(self):
        return self.user_type == 'B'

    @property
    def profile(self):
        try:
            return self.buyer_profile.get()
        except BuyerProfile.DoesNotExist:
            return None

    @property
    def subscriptions(self):
        if self.is_admin:
            return None
        return self.profile.subscriptions


class BuyerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_profile')
    billing_day = models.DateField(auto_now_add=True)  # change here
    payment_authorized = models.BooleanField(default=False)
    subscriptions = models.ManyToManyField('Subscription', related_name='buyer', blank=True)
    transactions = models.ManyToManyField('Transaction', related_name='buyer', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() if self.user.get_full_name() else self.user.email}'s profile"

    @property
    def label(self):
        return str(self)


class Transaction(models.Model):
    subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, related_name='transaction', null=True,
                                     blank=False)


class Subscription(models.Model):
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, related_name='subscription', null=True, blank=False)

    def __str__(self):
        return str(self.plan)


class Plan(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    monthly_fee = models.PositiveIntegerField(blank=False, null=False, default=0)
    features = models.ManyToManyField('Feature', related_name='plan')

    def __str__(self):
        return f"[ {self.name} ] Plan for {self.monthly_fee}$"


class Feature(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=50, blank=False, null=False)
    unit_price = models.PositiveIntegerField(blank=False, null=False, default=0)
    max_unit_limit = models.PositiveIntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Usage(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usage')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='usage')
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True, related_name='usage')
    unit_used = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.subscription.plan.name}] -- [{self.feature.name}] usage by {self.buyer}'
