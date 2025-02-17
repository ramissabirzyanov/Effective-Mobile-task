from order_app.order.models import OrderItem
from order_app.item.models import Item
from django.shortcuts import get_object_or_404


class OrderService:
    """
    Добавляет товары в заказ на основе данных из запроса.
    Возвращает True, если хотя бы один товар был добавлен.
    """
    @staticmethod
    def check_items(order, request):
        order_items = []
        for key, quantity in request.items():
            if key.startswith('item_') and quantity.isdigit():
                item_id = key.split('_')[1]
                quantity=int(quantity)
                if quantity <= 0:
                    continue
                item = get_object_or_404(Item, id=item_id)
                order_items.append(OrderItem(order=order, item=item, quantity=quantity))
        return order_items
    
    @staticmethod
    def update_quantity(order, request):
        items_to_update = []
        added_order_items = OrderItem.objects.filter(order=order)
        for order_item in added_order_items:
            quantity =  request.get(f'item_{order_item.item.id}')
            if quantity and int(quantity) > 0:
                order_item.quantity += int(quantity)
                items_to_update.append(order_item)
        return items_to_update
