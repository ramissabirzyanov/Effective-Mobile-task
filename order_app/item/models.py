from django.db import models


class Item(models.Model):
    """
    Модель для позиций, которые будут добавляться в заказ.
    """

    name = models.CharField(unique=True, verbose_name='item_name')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'item'
        verbose_name = 'item'

    def __str__(self):
        return self.name
