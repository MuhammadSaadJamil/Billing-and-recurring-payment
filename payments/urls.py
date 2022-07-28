from django.urls import path
from payments.views import *

urlpatterns = [
    path('authorize', authorize_payment, name='authorize-payment')
]
