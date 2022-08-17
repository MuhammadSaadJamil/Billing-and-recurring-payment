from django.shortcuts import render
from rest_framework import routers
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from base.models import *


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class FeatureViewSet(ModelViewSet):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()


class ListBuyers(ListAPIView):
    serializer_class = BuyerSerializer
    queryset = User.objects.get_buyers()


router = routers.SimpleRouter()
router.register(r'plans', PlanViewSet)
router.register(r'features', FeatureViewSet)
