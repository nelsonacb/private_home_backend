from rest_framework import serializers
from .models import Booking
from apps.users.serializers import UserSerializer
from apps.properties.serializers import RoomSerializer, PropertyListSerializer

class BookingListSerializer(serializers.ModelSerializer):
    guest_email = serializers.EmailField(source='guest.email', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True, default=None)
    property_name = serializers.CharField(source='property.name', read_only=True, default=None)

    class Meta:
        model = Booking
        fields = [
            'id', 'guest', 'guest_email', 'room', 'room_number',
            'property', 'property_name', 'check_in', 'check_out',
            'number_of_guests', 'status', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_price']

class BookingDetailSerializer(BookingListSerializer):
    """Serializer detallado con objetos anidados."""
    guest_details = UserSerializer(source='guest', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    property_details = PropertyListSerializer(source='property', read_only=True)

    class Meta(BookingListSerializer.Meta):
        fields = BookingListSerializer.Meta.fields + [
            'guest_details', 'room_details', 'property_details', 'notes'
        ]

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'room', 'property', 'check_in', 'check_out',
            'number_of_guests', 'notes'
        ]

    def validate(self, attrs):
        room = attrs.get('room')
        property = attrs.get('property')
        if not room and not property:
            raise serializers.ValidationError("Debe especificar room o property.")
        if room and property:
            raise serializers.ValidationError("Debe especificar solo uno: room o property.")
        if attrs['check_out'] <= attrs['check_in']:
            raise serializers.ValidationError("La fecha de salida debe ser posterior a la de entrada.")
        return attrs

    def create(self, validated_data):
        # El guest se asigna en la vista (request.user)
        validated_data['guest'] = self.context['request'].user
        return super().create(validated_data)