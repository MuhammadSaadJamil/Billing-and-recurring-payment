from django.urls import path
from .views import *

urlpatterns = [
    path('subscriptions/<int:pk>/', get_subscriptions, name='list-subscriptions'),
    path('user/<int:pk>/', get_feature_usage, name='list-usage'),
    path('admin/update/<int:pk>', UpdateUsage.as_view(), name='update-usage')

]
