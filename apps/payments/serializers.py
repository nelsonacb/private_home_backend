from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer para pagos."""
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)
    guest_email = serializers.EmailField(source='booking.guest.email', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'booking_id', 'guest_email', 'amount',
            'payment_date', 'method', 'method_display', 'reference',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'payment_date', 'created_at', 'updated_at']