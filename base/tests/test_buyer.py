from django.test import TestCase
from base.models import User, BuyerProfile


# Create your tests here.
class BuyerTestCase(TestCase):
    def setUp(self):
        buyer = User.objects.create(email='test@djangotest.com', user_type='B')
        buyer.set_password("test1234")
        BuyerProfile.objects.create(user=buyer)
        buyer.save()

    def test_buyer_is_not_admin(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertTrue(buyer.is_buyer)
        self.assertFalse(buyer.is_admin)

    def test_buyer_has_profile(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertIsNotNone(buyer.profile)

    def test_buyer_profile_completion(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertFalse(buyer.is_complete)

    def test_buyer_amount_due(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(buyer.amount_due['total'], 0)

    def test_buyer_subscriptions(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(len(buyer.subscriptions.all()), 0)

    def test_buyer_transactions(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(len(buyer.transactions.all()), 0)

    def test_buyer_string_representation(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(str(buyer), buyer.email)
        buyer.first_name = 'test'
        buyer.save()
        self.assertEqual(str(buyer), buyer.first_name)

    def test_buyer_profile_representation(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(str(buyer.profile), f"{buyer.email}'s profile")

    def test_buyer_profile_label(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(buyer.profile.label, f"{buyer.email}'s profile")

    def test_buyer_payment_auth(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertFalse(buyer.profile.payment_authorized)
        profile = buyer.profile
        profile.stripe_token = 'test'
        profile.save()
        self.assertTrue(buyer.profile.payment_authorized)
