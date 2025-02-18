from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order_app.order.views import OrdersAPIView
from order_app.item.views import ItemAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


router = DefaultRouter()
router.register(r'api/orders', OrdersAPIView)
router.register(r'api/items', ItemAPIView)

schema_view = get_schema_view(
    openapi.Info(title="API Documentation", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-doc"),
    path('orders/', include('order_app.order.urls')),
    path('items/', include('order_app.item.urls')),
    
]

urlpatterns += [
    path('', include(router.urls))
]
