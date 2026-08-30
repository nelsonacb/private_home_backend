import django_filters
from .models import Booking

class BookingFilter(django_filters.FilterSet):
    guest_email = django_filters.CharFilter(field_name='guest__email', lookup_expr='icontains')
    property_name = django_filters.CharFilter(field_name='property__name', lookup_expr='icontains')
    room_number = django_filters.CharFilter(field_name='room__room_number', lookup_expr='icontains')
    check_in_after = django_filters.DateFilter(field_name='check_in', lookup_expr='gte')
    check_in_before = django_filters.DateFilter(field_name='check_in', lookup_expr='lte')
    check_out_after = django_filters.DateFilter(field_name='check_out', lookup_expr='gte')
    check_out_before = django_filters.DateFilter(field_name='check_out', lookup_expr='lte')
    status = django_filters.ChoiceFilter(choices=Booking.BookingStatus.choices)
    min_total = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_total = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')

    class Meta:
        model = Booking
        fields = [
            'guest_email', 'property_name', 'room_number',
            'check_in_after', 'check_in_before', 'check_out_after', 'check_out_before',
            'status', 'min_total', 'max_total'
        ]