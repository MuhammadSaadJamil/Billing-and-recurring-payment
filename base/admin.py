from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Subscription)
admin.site.register(Plan)
admin.site.register(Feature)


@admin.register(BuyerProfile)
class ProfileManager(admin.ModelAdmin):
    list_display = ['label', 'billing_day', 'payment_authorized']
