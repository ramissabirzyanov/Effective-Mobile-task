from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.views import FilterView
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .forms import OrderCreateForm, OrderItemForm
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


class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'order/order_create.html'
    success_message = 'Order has been created'
    success_url = reverse_lazy('orders')


    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.calculate_total_price()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_item_form'] = OrderItemForm()
        return context
