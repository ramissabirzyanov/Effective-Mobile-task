from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrdersListView.as_view(), name='orders'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('revenue/', views.TotalRevenueView.as_view(), name='total_revenue'),
]
