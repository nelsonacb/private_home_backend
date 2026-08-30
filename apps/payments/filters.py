import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    """Filtros para pagos."""
    booking_id = django_filters.NumberFilter(field_name='booking__id')
    guest_email = django_filters.CharFilter(field_name='booking__guest__email', lookup_expr='icontains')
    method = django_filters.ChoiceFilter(choices=Payment.PaymentMethod.choices)
    date_from = django_filters.DateFilter(field_name='payment_date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='payment_date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = Payment
        fields = [
            'booking_id', 'guest_email', 'method',
            'date_from', 'date_to', 'min_amount', 'max_amount'
        ]