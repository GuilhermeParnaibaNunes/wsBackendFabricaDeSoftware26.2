from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product

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
        form = ProductForm(initial=request.GET)

    return render(request, 'inventory/register.html', {'form': form})