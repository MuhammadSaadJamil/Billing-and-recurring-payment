from django.urls import path
from .views import *

urlpatterns = [
    path('user/<int:pk>/', get_transactions, name='list-transactions'),

]
