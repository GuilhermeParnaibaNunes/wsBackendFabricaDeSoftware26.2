from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
import requests

@login_required
def inventory(request):
    products = Product.objects.filter(store=request.user)
    
    return render(request, 'inventory/inventory.html', {'products': products})

@login_required
def register_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            # Security measure: Stages the form save until user is registered
            new_product = form.save(commit=False)
            new_product.store = request.user
            new_product.save()
            
            return redirect('inventory') 
    else:
        form = ProductForm(initial=request.GET.dict())

    return render(request, 'inventory/register.html', {'form': form})

@login_required
def product_detail(request, sku):
    product = get_object_or_404(Product, sku=sku, store=request.user)
    return render(request, 'inventory/detail.html', {'product': product})

@login_required
def product_update(request, sku):
    product = get_object_or_404(Product, sku=sku, store=request.user)

    if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_detail', sku=product.sku)
    else:
        form = ProductForm(instance=product)
            
    return render(request, 'inventory/update.html', {'form': form, 'product': product})

@login_required
def product_delete(request, sku):
    product = get_object_or_404(Product, sku=sku, store=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('inventory')

    return render(request, 'inventory/delete.html', {'product': product})

@login_required
def search_api(request):
    query = request.GET.get('q')
    results = []

    if query:
        url = f"https://dummyjson.com/products/search?q={query}"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            results = json_data.get('products', [])

    return render(request, 'inventory/search_api.html', {
        'results': results, 
        'query': query
    })