from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('admin/register', admin_signup, name='admin-signup'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('profile/update/<str:uidb64>', update_profile, name='update-profile'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
