import django_filters
from .models import Property, Room

class PropertyFilter(django_filters.FilterSet):
    """Filtros para propiedades."""
    name = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    province = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    min_guests = django_filters.NumberFilter(field_name='max_guests', lookup_expr='gte')
    is_active = django_filters.BooleanFilter()
    # Filtro por propietario (email)
    owner_email = django_filters.CharFilter(field_name='owner__email', lookup_expr='icontains')

    class Meta:
        model = Property
        fields = ['name', 'city', 'province', 'min_price', 'max_price', 'min_guests', 'is_active', 'owner_email']

class RoomFilter(django_filters.FilterSet):
    """Filtros para habitaciones."""
    property_name = django_filters.CharFilter(field_name='property__name', lookup_expr='icontains')
    room_type = django_filters.ChoiceFilter(choices=Room.ROOM_TYPES)
    min_capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Room
        fields = ['property', 'property_name', 'room_type', 'min_capacity', 'min_price', 'max_price', 'is_available']