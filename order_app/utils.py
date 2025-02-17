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