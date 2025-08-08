from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('products/<int:product_id>/cart_actions/', views.cart_actions, name='cart_actions'),





]
