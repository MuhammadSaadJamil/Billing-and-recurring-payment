from django.urls import path
from buyer.views.views import *
from buyer.views.subscription_views import *

urlpatterns = [
    path('feature/<int:pk>', DetailFeature.as_view(), name='feature-details'),
    path('subscription/subscribe/<int:pk>', subscribe, name='subscribe'),
]
