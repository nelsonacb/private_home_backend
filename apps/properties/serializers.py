from rest_framework import serializers
from .models import Property, Room
from apps.users.serializers import UserSerializer  # Para mostrar info del propietario

class RoomSerializer(serializers.ModelSerializer):
    """Serializer para habitaciones."""
    property_name = serializers.CharField(source='property.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'property', 'property_name', 'room_number', 'room_type',
            'capacity', 'price_per_night', 'description', 'amenities',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PropertyListSerializer(serializers.ModelSerializer):
    """Serializer para listado de propiedades (sin habitaciones)."""
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.SerializerMethodField()
    total_rooms = serializers.IntegerField(source='rooms.count', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'description', 'address', 'city', 'province',
            'price_per_night', 'max_guests', 'services', 'owner', 'owner_email',
            'owner_name', 'total_rooms', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_owner_name(self, obj):
        return obj.owner.get_full_name()

class PropertyDetailSerializer(PropertyListSerializer):
    """Serializer detallado que incluye habitaciones anidadas."""
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta(PropertyListSerializer.Meta):
        fields = PropertyListSerializer.Meta.fields + ['rooms']