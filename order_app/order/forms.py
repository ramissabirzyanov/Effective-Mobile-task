from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'status']


class OrderStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']
