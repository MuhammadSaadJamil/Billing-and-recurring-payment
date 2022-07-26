from django.urls import path
from .views import *

urlpatterns = [
    path('subscriptions/<int:pk>/', get_subscriptions, name='list-subscriptions'),
    path('usage/<int:pk>/', get_feature_usage, name='list-usage'),
    path('admin/usage/update/<int:pk>', UpdateUsage.as_view(), name='update-usage')

]
