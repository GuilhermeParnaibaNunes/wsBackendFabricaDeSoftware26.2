from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, SaleForm
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
    error_message = None

    if query:
        # Defensive Exchange Rate (1-second timeout)
        exchange_rate = 5.50 # Fixed fallback in case of internet instability
        try:
            rate_response = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL", timeout=1)
            if rate_response.status_code == 200:
                rate_data = rate_response.json()
                exchange_rate = float(rate_data['USDBRL']['bid'])
        except requests.exceptions.RequestException:
            pass # Silent failure: swallows the error and uses the R$ 5.50 fallback

        # Global API Lookup (3-second timeout)
        try:
            url = f"https://dummyjson.com/products/search?q={query}"
            response = requests.get(url)

            if response.status_code == 200:
                json_data = response.json()
                raw_results = json_data.get('products', [])

                # Price conversion before injection into HTML
                for p in raw_results:
                    converted_price = float(p.get('price', 0)) * exchange_rate
                    p['price_brl'] = round(converted_price, 2)
                    results.append(p)
            else:
                error_message = "> ERRO_NO_SERVIDOR_GLOBAL: A base de dados recusou a conexão."

        # Catches any internet outages or server timeouts
        except:
            error_message = "> FALHA_DE_SINAL: Impossível conectar à base global no momento."

    return render(request, 'inventory/search_api.html', {
        'results': results, 
        'query': query,
        'error_message': error_message
    })

@login_required
def sell_product(request):
    if request.method == 'POST':
        # Request.user is passed to filter form list 
        form = SaleForm(request.POST, user=request.user)
        
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product
            
            # Safety lock: prevents selling more than is in stock
            if sale.quantity_sold > product.amount:
                form.add_error('quantity_sold', f"> ERRO: Estoque insuficiente. Restam {product.amount} unidades.")
            else:
                # Calculates the sale total mathematically
                sale.total_value = sale.quantity_sold * product.unitary_price
                sale.store = request.user
                
                # Manages finances and inventory
                product.amount -= sale.quantity_sold
                request.user.balance += sale.total_value
                
                # Commits the three changes to the database
                product.save()
                request.user.save()
                sale.save()
                
                return redirect('inventory')
    else:
        form = SaleForm(user=request.user)

    return render(request, 'inventory/sell_product.html', {'form': form})