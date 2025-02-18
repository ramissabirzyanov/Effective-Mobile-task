from django.contrib import admin
from .models import Item


@admin.register(Item)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
