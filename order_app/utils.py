from order_app.order.models import Order, OrderItem
from order_app.item.models import Item
from django.shortcuts import get_object_or_404
from django.views import View



class OrderService:
    """
    Добавляет товары в список на основе данных из запроса.
    Возвращает список товаров, которые нужно добавить в зазаз.
    """
    @staticmethod
    def add_new_items(order: Order, request: dict) -> list[OrderItem]:
        order_items = []
        existing_item_ids = set(OrderItem.objects.filter(order=order).values_list("item_id", flat=True))
        for key, quantity in request.items():
            if key.startswith('item_') and quantity.isdigit():
                item_id = int(key.split('_')[1])
                quantity=int(quantity)
                if quantity > 0 and item_id not in existing_item_ids:
                    item = get_object_or_404(Item, id=item_id)
                    order_items.append(OrderItem(order=order, item=item, quantity=quantity))
        return order_items

    @staticmethod
    def update_quantity(order: Order, request: dict) -> list[OrderItem]:
        items_to_update = []
        added_order_items = OrderItem.objects.filter(order=order)
        for order_item in added_order_items:
            quantity = int(request.get(f'item_{order_item.item.id}', 0))
            if quantity > 0:
                order_item.quantity += quantity
                items_to_update.append(order_item)
        return items_to_update


class OrderContextMixin(View):
    """
    Миксин для добавления списка товаров в контекст.
    """
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        return context