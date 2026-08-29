from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ShopkeeperCreationForm

def register_account(request):
    if request.user.is_authenticated:
        return redirect('inventory')
    
    if request.method == 'POST':
        form = ShopkeeperCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ShopkeeperCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
