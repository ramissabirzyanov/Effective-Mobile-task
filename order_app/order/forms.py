from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'status']


class OrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number','status']
