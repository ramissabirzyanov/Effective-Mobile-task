from django.forms import ModelForm
from .models import Item


class ItemCreateForm(ModelForm):
    """
    Форма для создания новой позиции (item).
    """

    class Meta:
        model = Item
        fields = ['name', 'price']
