from django.urls import path
from .views import home, about_page, products_page, product_page , manage_products, seller_products, add_product, delete_product, edit_product, admin_manage_products
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', home, name='Home'),
    path('about/', about_page, name='about'),
    path('products/', products_page, name='products'),
    path('product/', product_page, name='product'),
    path('products/<int:pk>/', product_page, name='product'),
    path('accounts/logout/', LogoutView.as_view(next_page='Home'), name='logout'),
    path('dashboard/products/', manage_products, name='manage_products'),
    path('my-products/', seller_products, name='my_products'),
    path('add-product/', add_product, name='add_product'),
    path('seller/products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('seller/products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('manage/products/', admin_manage_products, name='admin_products'),



]
