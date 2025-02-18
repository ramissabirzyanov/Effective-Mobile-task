import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    table_number = django_filters.NumberFilter(field_name='table_number', label='Номер стола')
    status = django_filters.ChoiceFilter(choices=Order.STATUS_CHOICES, label='Статус')

    class Meta:
        model = Order
        fields = ['table_number', 'status']
