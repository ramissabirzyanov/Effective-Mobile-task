from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.views import FilterView
from .models import Order, OrderItem
from order_app.item.models import Item
from .serializers import OrderSerializer
from .forms import OrderCreateForm
from .filters import OrderFilter


class OrdersAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['table_number', 'status']


class OrdersListView(FilterView):
    queryset = Order.objects.all()
    template_name = 'order/orders.html'
    filterset_class = OrderFilter
    context_object_name = 'orders'


class OrderCreateView(views.SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'order/order_create.html'
    success_message = 'Order has been created'
    success_url = reverse_lazy('orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        return context

    def form_valid(self, form):
        try:
            response = super().form_valid(form)  # Создаем заказ
            order = self.object  # Получаем созданный заказ

            for key, quantity in self.request.POST.items():
                if key.startswith('item_') and quantity.isdigit():
                    item_id = key.split('_')[1]
                    item = Item.objects.get(id=item_id)
                    if int(quantity) > 0:
                        OrderItem.objects.create(order=order, item=item, quantity=int(quantity))
            order.calculate_total_price()
            return response
        except Item.DoesNotExist:
                    self.object.delete()  # Откат, если товар не найден
                    messages.ERROR(self.request, "There is no such item.")
                    return self.form_invalid(form)
                
        except ValueError:
                    self.object.delete()  # Откат, если количество — не число
                    messages.ERROR(self.request, "Check quantity")
                    return self.form_invalid(form)
