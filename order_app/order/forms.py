from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма для создания заказа.
    """
    class Meta:
        model = Order
        fields = ['table_number', 'status']


class OrderUpdateForm(forms.ModelForm):
    """
    Форма для обновления заказа.
    """
    class Meta:
        model = Order
        fields = ['table_number','status']
