from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', lambda request: render(request, 'orders/order_success.html'), name='order_success'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('admin/all-orders/', views.admin_all_orders_view, name='admin_all_orders'),
    path('admin/orders/status-toggle/<int:order_id>/', views.toggle_order_status, name='toggle_order_status'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
    


    



]
