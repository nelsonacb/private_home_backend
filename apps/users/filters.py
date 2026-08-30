import django_filters
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()

class UserFilter(django_filters.FilterSet):
    """Filtros para el modelo User."""
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.ChoiceFilter(choices=Role.choices)
    is_active = django_filters.BooleanFilter()
    date_joined = django_filters.DateFromToRangeFilter()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'is_active']