from django.urls import path, include
from .views import *

urlpatterns = [
    path('', include(router.urls)),
    path('buyers', ListBuyers.as_view()),
]
