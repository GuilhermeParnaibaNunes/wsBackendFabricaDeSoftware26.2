"""
URL configuration for Pyventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from inventory import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth routes
    path('account/register/', accounts_views.register_account, name='register_account'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Main route (Home)
    path('', inventory_views.inventory, name='inventory'),

    # Inventory routes
    path('product/register/', inventory_views.register_product, name='register_product'),
    path('product/detail/<str:sku>/', inventory_views.product_detail, name='product_detail'),
    path('product/update/<str:sku>/', inventory_views.product_update, name='product_update'),
    path('product/delete/<str:sku>/', inventory_views.product_delete, name='product_delete'),
]
