from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def home(request):
    return render(request, 'furniture/home.html')

def about_page(request):
    return render(request, 'pages/about.html')

def products_page(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'furniture/products.html', {'products': products})

def product_page(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return render(request, 'furniture/noproduct.html')

    return render(request, 'furniture/product.html', {'product': product})


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


