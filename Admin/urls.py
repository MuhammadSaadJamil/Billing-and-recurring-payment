from django.urls import path, re_path
from .views.feature_views import *
from .views.plan_views import *
from .views.user_views import *

urlpatterns = [
    # Plan URLS
    path('plans/', ListPlan.as_view(), name='list-plan'),
    path('plans/add', CreatePlan.as_view(), name='add-plan'),
    path('plans/<int:pk>', DetailPlan.as_view(), name='get-plan'),
    path('plans/update/<int:pk>', UpdatePlan.as_view(), name='update-plan'),
    path('plans/delete/<int:pk>', DeletePlan.as_view(), name='delete-plan'),
    # Feature URLS
    path('features/', ListFeature.as_view(), name='list-plan'),
    path('features/add', CreateFeature.as_view(), name='add-plan'),
    path('features/<int:pk>', DetailFeature.as_view(), name='get-plan'),
    path('features/update/<int:pk>', UpdateFeature.as_view(), name='update-plan'),
    path('features/delete/<int:pk>', DeleteFeature.as_view(), name='delete-plan'),
    # User Views
    path('buyers', ListBuyers.as_view(), name='list-buyers')
]
