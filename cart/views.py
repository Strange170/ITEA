from django.shortcuts import get_object_or_404, redirect, render
from furniture.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


@login_required
def cart_actions(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, product.in_stock))  # تأكد الكمية ضمن الحد

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        new_quantity = cart_item.quantity + quantity
        cart_item.quantity = min(new_quantity, product.in_stock)
    else:
        cart_item.quantity = quantity
    cart_item.save()

    action = request.POST.get('action')

    if action == 'buy_now':
        return redirect('checkout')
    else:
        return redirect('cart_view')



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total_price = sum(item.get_total_price() for item in items)

    return render(request, 'cart/cart.html', {
        'cart_items': items,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart_view')

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if item.quantity < item.product.in_stock:
        item.quantity += 1
        item.save()
    else:
        item.quantity = item.product.in_stock  
        item.save()
    return redirect('cart_view')

