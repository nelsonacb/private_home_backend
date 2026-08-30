from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para opiniones."""
    guest_email = serializers.EmailField(source='booking.guest.email', read_only=True)
    property_name = serializers.CharField(source='property.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'booking', 'guest_email', 'property', 'property_name',
            'room', 'room_number', 'rating', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Verificar que el huésped que opina es el de la reserva
        request = self.context.get('request')
        booking = data.get('booking')
        if request and booking and request.user != booking.guest and request.user.role not in ['admin', 'owner']:
            raise serializers.ValidationError("Solo el huésped de la reserva puede opinar.")
        return data