from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from furniture.models import Product
from django.db.models import Sum


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']
        total_price = sum(item.get_total_price() for item in items)

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

        cart.items.all().delete()

        return redirect('order_success')

    return render(request, 'orders/checkout.html', {'cart_items': items})


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

@user_passes_test(is_admin)
def admin_all_orders_view(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/admin_all_orders.html', {'orders': orders})