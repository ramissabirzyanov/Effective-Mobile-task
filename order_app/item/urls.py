from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/items', views.ItemAPIView)

urlpatterns = [
    path('', views.ItemListView.as_view(), name='items'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
]
