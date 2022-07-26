"""RecurringPayment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from base.views import *

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('', index, name='home'),
    path('user/profile', get_profile, name='profile'),
    path('unauthorized/', unauthorized, name='err-401'),
    path('accounts/', include("accounts.urls")),
    path('admin/', include("base_admin.urls")),
    path('user/', include("buyer.urls")),
    path('usage/', include("usage.urls")),
    path('payment/', include("payments.urls")),
    path('transactions/', include("transactions.urls")),
    path('api/', include("api.urls")),
    path('payment/error', card_error, name='payment-error'),
]
