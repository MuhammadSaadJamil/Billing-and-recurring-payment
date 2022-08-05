from django.test import TestCase
from base.models import User, BuyerProfile, Subscription, Plan, Feature, Usage


# Create your tests here.
class BuyerSubscriptionTestCase(TestCase):
    def setUp(self):
        buyer = User.objects.create(email='test@djangotest.com', user_type='B')
        buyer.set_password("test1234")
        BuyerProfile.objects.create(user=buyer)
        buyer.save()
        # creating feature
        feature = Feature.objects.create(name='test', unit_price=2, max_unit_limit=20)
        # creating plan
        plan = Plan.objects.create(name='test', monthly_fee=200)
        plan.features.add(feature)
        plan.save()
        # creating subscription and adding to profile
        subscription = Subscription.objects.create(plan=plan)
        profile = buyer.profile
        profile.subscriptions.add(subscription)
        # creating usage
        usage = Usage.objects.create(buyer=buyer, subscription=subscription, feature=feature, unit_used=21)
        profile.save()

    def test_buyer_amount_due(self):
        buyer = User.objects.get(email='test@djangotest.com')
        self.assertEqual(buyer.amount_due['total'], 202)

    def test_buyer_reset_payment(self):
        buyer = User.objects.get(email='test@djangotest.com')
        buyer.reset_payment()
        self.assertEqual(buyer.amount_due['total'], 200)
