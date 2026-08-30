import django_filters
from .models import Review

class ReviewFilter(django_filters.FilterSet):
    """Filtros para opiniones."""
    guest_email = django_filters.CharFilter(field_name='booking__guest__email', lookup_expr='icontains')
    property_name = django_filters.CharFilter(field_name='property__name', lookup_expr='icontains')
    room_number = django_filters.CharFilter(field_name='room__room_number', lookup_expr='icontains')
    rating = django_filters.NumberFilter(field_name='rating')
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Review
        fields = [
            'guest_email', 'property_name', 'room_number', 'rating',
            'min_rating', 'max_rating', 'created_after', 'created_before'
        ]