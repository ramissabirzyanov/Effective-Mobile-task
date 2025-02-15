from django import forms
from .models import Order
from order_app.item.models import Item


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'status']


class OrderItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)


class OrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
