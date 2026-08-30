from django.db import models
from django.conf import settings

class Product(models.Model):
    # Foreign key: every product is owned by a store (User)
    store = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    # Main
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=128, default='')
    brand = models.CharField(max_length=128, blank=True, default='')
    
    # ID
    sku = models.CharField(max_length=30, unique=True)
    bar_code = models.CharField(
        max_length=14,
        unique=True,
    )
    
    # Stock & price
    amount = models.PositiveBigIntegerField(default=0)
    low_stock_level = models.PositiveBigIntegerField(default=5)
    unitary_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Auditing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - [{self.sku}]"
    
    @property
    def is_low_stock(self):
        return self.amount <= self.low_stock_level

class Sale(models.Model):
    # Foreign keys: every sale is relate 1 : 1 product/store (user)
    store = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sales')
    
    # Sale data
    buyer_name = models.CharField(max_length=128, blank=True, default="Cliente Padrão")
    quantity_sold = models.PositiveIntegerField(default=1)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Produto Excluído"
        return f"[{self.sale_date.strftime('%d/%m/%Y')}] {self.quantity_sold}x {product_name} - R$ {self.total_value}"
