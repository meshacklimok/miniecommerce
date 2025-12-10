
from django.contrib import admin
from .models import MpesaPayment

@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id', 'phone_number')
