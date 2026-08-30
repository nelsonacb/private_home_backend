from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_date', 'method', 'reference')
    list_filter = ('method', 'payment_date')
    search_fields = ('booking__guest__email', 'reference', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-payment_date',)