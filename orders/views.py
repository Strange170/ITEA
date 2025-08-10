from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from furniture.models import Product
from django.db.models import Sum


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total_price = sum(item.get_total_price() for item in items)  

    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=total_price,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            product = item.product
            product.in_stock -= item.quantity
            if product.in_stock < 0:
                product.in_stock = 0
            product.save()

        cart.items.all().delete()

        return redirect('order_success')

    return render(request, 'orders/checkout.html', {
        'cart_items': items,
        'total_price': total_price,
    })


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def seller_dashboard(request):
    if request.user.user_type != 'seller':
        return redirect('Home')

    products = Product.objects.filter(owner=request.user)

    product_names = []
    product_sales = []

    for product in products:
        total_sold = OrderItem.objects.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0
        product_names.append(product.name)
        product_sales.append(total_sold)

    return render(request, 'orders/seller_dashboard.html', {
        'labels': product_names,
        'data': product_sales
    })


def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'


def is_admin_or_seller(user):
    return user.is_authenticated and (user.user_type == 'admin' or user.user_type == 'seller')


@user_passes_test(is_admin)
def admin_all_orders_view(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/admin_all_orders.html', {'orders': orders})


@user_passes_test(is_admin_or_seller)
@login_required
def toggle_order_status(request, order_id):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        if request.user.user_type == 'admin':
            return redirect('admin_all_orders')
        return redirect('seller_orders')

    order = get_object_or_404(Order, id=order_id)

    if request.user.user_type == 'seller':
        seller_products = Product.objects.filter(owner=request.user)
        if not OrderItem.objects.filter(order=order, product__in=seller_products).exists():
            messages.error(request, "You don't have permission to change this order's status.")
            return redirect('seller_orders')

    if order.status == 'PENDING':
        order.status = 'COMPLETED'
    else:
        order.status = 'PENDING'
    order.save()
    messages.success(request, f"Order #{order.id} status changed to {order.status}")

    if request.user.user_type == 'admin':
        return redirect('admin_all_orders')
    else:
        return redirect('seller_orders')


@login_required
def seller_orders(request):
    if request.user.user_type != 'seller':
        return render(request, 'unauthorized.html')

    seller_products = Product.objects.filter(owner=request.user)
    
    order_items = OrderItem.objects.filter(product__in=seller_products).select_related('order', 'product')

    context = {
        'order_items': order_items
    }
    return render(request, 'orders/seller_orders.html', context)
