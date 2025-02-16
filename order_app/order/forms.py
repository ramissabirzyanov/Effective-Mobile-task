from django import forms
from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'status']


class OrderItemForm(forms.ModelForm):
    
    class Meta:
        model = OrderItem
        fields = ['quantity']
