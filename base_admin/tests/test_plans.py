from django.test import TestCase
from django.urls import reverse

from base.models import Plan, Feature, User


# Create your tests here.
class PlanTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@djangotest.com', user_type='A')
        admin.set_password('test')
        admin.save()
        feature = Feature.objects.create(name='test', code='ar2', unit_price=2, max_unit_limit=20)
        plan = Plan.objects.create(name='test plan', monthly_fee=200)
        plan.features.add(feature)
        plan.save()

    def test_plan_create_view(self):
        login = self.client.login(email='admin@djangotest.com', password='test')
        self.assertTrue(login)
        url = reverse("add-plan")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('form', str(resp.content))

    def test_plan_list_view(self):
        login = self.client.login(email='admin@djangotest.com', password='test')
        self.assertTrue(login)
        plan = Plan.objects.get(name="test plan")
        url = reverse("list-plan")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(plan.name, str(resp.content))

    def test_plan_update_view(self):
        login = self.client.login(email='admin@djangotest.com', password='test')
        self.assertTrue(login)
        plan = Plan.objects.get(name="test plan")
        url = reverse("update-plan", args=[plan.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_plan_delete_view(self):
        login = self.client.login(email='admin@djangotest.com', password='test')
        self.assertTrue(login)
        plan = Plan.objects.get(name="test plan")
        url = reverse("delete-plan", args=[plan.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_plan_detail_view(self):
        login = self.client.login(email='admin@djangotest.com', password='test')
        self.assertTrue(login)
        plan = Plan.objects.get(name="test plan")
        url = reverse("get-plan", args=[plan.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_plan_detail_view_error(self):
        login = self.client.login(email='admin@djangotest.com', password='test')
        self.assertTrue(login)
        url = reverse("get-plan", args=[200])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("not found", str(resp.content))
