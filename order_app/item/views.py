from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.viewsets import ModelViewSet
from .models import Item
from .serializers import ItemSerializer
from .forms import ItemCreateForm


class ItemAPIView(ModelViewSet):
    """
    API ViewSet для работы с позициями, которые можно добавить в заказ.
    Поддерживает стандартные CRUD-операции.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemListView(ListView):
    """
    View для отображения списка позиций.
    """
    queryset = Item.objects.all()
    template_name = 'item/items.html'


class ItemCreateView(SuccessMessageMixin, CreateView):
    """
    View для создания новой позиции.
    Обрабатывает форму создания позиции.
    """
    model = Item
    template_name = 'item/item_create.html'
    form_class = ItemCreateForm
    success_url = reverse_lazy('items')
    success_message = 'Item has been added'
