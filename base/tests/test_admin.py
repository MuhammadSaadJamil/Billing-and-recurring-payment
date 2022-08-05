from django.test import TestCase
from base.models import User, BuyerProfile


# Create your tests here.
class AdminTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@djangotest.com', user_type='A')

    def test_admin_does_not_have_profile(self):
        admin = User.objects.get(email='admin@djangotest.com')
        self.assertIsNone(admin.profile)

    def test_admin_does_not_have_subscriptions(self):
        admin = User.objects.get(email='admin@djangotest.com')
        self.assertIsNone(admin.subscriptions)

    def test_admin_does_not_have_transactions(self):
        admin = User.objects.get(email='admin@djangotest.com')
        self.assertIsNone(admin.transactions)

