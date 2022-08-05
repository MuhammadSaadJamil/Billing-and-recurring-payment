from django.test import TestCase
from base.models import Feature


# Create your tests here.
class FeatureTestCase(TestCase):
    def setUp(self):
        feature = Feature.objects.create(name='test', code='ar2', unit_price=2, max_unit_limit=20)

    def test_feature_representation(self):
        feature = Feature.objects.get(name='test')
        self.assertEqual(str(feature), f"{feature.code} - {feature.name}")
