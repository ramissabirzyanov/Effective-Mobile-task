from rest_framework import serializers
from order_app.item.serializers import ItemSerilizer
from .models import Order, OrderItem
from order_app.item.models import Item


class OrderItemsSerializer(serializers.ModelSerializer):
    item = ItemSerilizer()
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(), many=True)

    class Meta:
        model = Order
        fields = '__all__'


    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        print(items_data)
        for item_data in items_data:
            try:
                print(item_data)
                item = Item.objects.get(id=item_data['id'])
                price = item.price * item_data["quantity"]
                total_price = order.total_price + price
                order.total_price = total_price
            except Item.DoesNotExist:
                raise serializers.ValidationError(f"Item with ID {item_data['id']} does not exist.")
            order.items.add(item)
        order.save()
        return order