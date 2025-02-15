from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order_app.order.views import OrdersAPIView
from order_app.item.views import ItemAPIView


router = DefaultRouter()
router.register(r'api/orders', OrdersAPIView)
router.register(r'api/items', ItemAPIView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include('order_app.item.urls')),
    path('orders/', include('order_app.order.urls')),
]

urlpatterns += router.urls