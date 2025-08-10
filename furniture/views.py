from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.db.models import Sum, Q
from django.db.models.functions import Random
from django.core.paginator import Paginator



def home(request):
    return render(request, 'furniture/home.html')


def about_page(request):
    return render(request, 'pages/about.html')


def products_page(request):
    products_list = Product.objects.all().order_by('-created_at')

    query = request.GET.get('q', '')
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(subcategory__icontains=query)
        )

    price = request.GET.get('price')
    if price:
        if '-' in price:
            min_price, max_price = price.split('-')
            products_list = products_list.filter(price__gte=min_price, price__lte=max_price)
        elif '+' in price:
            min_price = price.replace('+', '')
            products_list = products_list.filter(price__gte=min_price)

    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    if 'page' in params:
        params.pop('page')

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'price': price,
        'query': query,
        'params': params.urlencode()
    }
    return render(request, 'furniture/products.html', context)


def product_page(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return render(request, 'furniture/noproduct.html')

    bestseller_products = Product.objects.annotate(
        total_sold=Sum('order_items_orders__quantity')
    ).order_by('-total_sold')[:3]

    related_products = Product.objects.filter(
        subcategory=product.subcategory
    ).exclude(id=product.id).order_by(Random())[:4]

    context = {
        'product': product,
        'bestseller_products': bestseller_products,
        'related_products': related_products,
    }
    return render(request, 'furniture/product.html', context)


@login_required
def manage_products(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'furniture/manage_products.html', {'products': products})


def products_by_owner(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'furniture/products.html', {'products': products})


@login_required
def seller_products(request):
    seller = request.user
    products = Product.objects.filter(owner=seller)
    return render(request, 'furniture/seller_products.html', {'products': products})


@login_required
def add_product(request):
    if request.user.user_type != 'seller':
        return redirect('Home')  # لو مش seller

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('my_products')
    else:
        form = ProductForm()

    return render(request, 'furniture/add_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    if request.user.user_type == 'admin':
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            product.delete()
        return redirect('admin_products')
    else:
        product = get_object_or_404(Product, pk=pk, owner=request.user)
        if request.method == 'POST':
            product.delete()
        return redirect('my_products')


@login_required
def edit_product(request, pk):
    if request.user.user_type == 'admin':
        product = get_object_or_404(Product, pk=pk)
    else:
        product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            if request.user.user_type == 'admin':
                return redirect('admin_products')
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'furniture/edit_product.html', {'form': form, 'product': product})


@staff_member_required
def admin_manage_products(request):
    products = Product.objects.all()
    return render(request, 'furniture/admin_products.html', {'products': products})


def charts_page(request):
    return render(request, 'dashboard/charts.html')
