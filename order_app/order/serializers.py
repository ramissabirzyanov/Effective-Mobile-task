from rest_framework import serializers
from .models import Order, OrderItem
from order_app.item.models import Item
from order_app.utils import OrderService


def _post_data_to_request_format(items_data):
    """
    Конвертирует данные API в формат, совместимый с OrderService.
    На выходе: {"item_1": 2, "item_2": 3}
    """
    return {f"item_{item['item'].id}": str(item["quantity"]) for item in items_data}


class OrderItemsSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    quantity = serializers.IntegerField(min_value=0)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(source='order_items', many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True) 
    table_number = serializers.IntegerField(min_value=0)
    
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'total_price', 'items'] 

    def create(self, validated_data):
        print(validated_data)
        items_data = validated_data.pop('order_items', []) 
        order = Order.objects.create(**validated_data)
        request_like_data = _post_data_to_request_format(items_data)
        items_added = OrderService.add_new_items(order, request_like_data)
        if not items_added:
            raise "Can't create order with no any items"
        OrderItem.objects.bulk_create(items_added)
        order.calculate_total_price()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        instance = super().update(instance, validated_data)
        request_like_data = _post_data_to_request_format(items_data)
        items_to_update = OrderService.update_quantity(instance, request_like_data)
        if items_to_update:
            OrderItem.objects.bulk_update(items_to_update, ['quantity'])
        new_items = OrderService.add_new_items(instance, request_like_data)
        if new_items:
            OrderItem.objects.bulk_create(new_items)
        instance.calculate_total_price()
        return instance
