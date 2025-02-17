from django.db import models
from order_app.item.models import Item


class Order(models.Model):
    
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('done', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(unique=True, verbose_name='table_number')
    items = models.ManyToManyField(Item, related_name='orders', through='OrderItem', verbose_name='items')
    total_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='total_price', default=0)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='status', default='waiting')

    class Meta:
        ordering = ['id']
        db_table = 'order'
        verbose_name = 'order'
    
    def calculate_total_price(self):
        total = sum(order_item.get_item_price() for order_item in self.order_items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id}, table {self.table_number}. Status {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_item_price(self):
        return self.item.price * self.quantity
