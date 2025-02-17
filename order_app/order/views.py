from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.views import FilterView
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .forms import OrderCreateForm, OrderUpdateForm
from .filters import OrderFilter
from django.core.exceptions import ValidationError
from order_app.utils import OrderService, OrderContextMixin
from django.db.models import Sum



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


class OrderCreateView(OrderContextMixin, views.SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'order/order_create.html'
    success_message = 'Order has been created'
    success_url = reverse_lazy('orders')

    def form_valid(self, form):
        try:
            response = super().form_valid(form) 
            order = self.object
            items_added = OrderService.add_new_items(order, self.request.POST)
            if not items_added:
                order.delete()
                raise ValidationError("You can't create an order without any item")
            OrderItem.objects.bulk_create(items_added)
            order.calculate_total_price()
            return response
                
        except ValueError:
            self.object.delete()
            messages.error(self.request, "Check quantity")
            return self.form_invalid(form)


class OrderUpdateView(OrderContextMixin, views.SuccessMessageMixin, UpdateView):
    model=Order
    form_class=OrderUpdateForm
    template_name='order/order_update.html'
    success_message='Order has been changed'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance = self.get_object()
        return form

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        items_to_update = OrderService.update_quantity(order, self.request.POST)
        if items_to_update:
            OrderItem.objects.bulk_update(items_to_update, ['quantity'])
        new_items = OrderService.add_new_items(order, self.request.POST)
        if new_items:
            OrderItem.objects.bulk_create(new_items)
        order.calculate_total_price()
        return response
    

class OrderDetailView(DetailView):
    model = Order
    template_name='order/order_detail.html'


class OrderDeleteView(views.SuccessMessageMixin, DeleteView):
    model=Order
    template_name='order/order_delete.html'
    success_message='Order was deleted'
    success_url= reverse_lazy('orders')


class TotalRevenueView(TemplateView):
    template_name='order/total_revenue.html'

    def get_context_data(self, **kwargs):
        paid_orders = Order.objects.filter(status='paid')
        total_revenue = paid_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0 
        context = super().get_context_data(**kwargs)
        context['paid_orders'] = paid_orders
        context['total_revenue'] = total_revenue
        return context