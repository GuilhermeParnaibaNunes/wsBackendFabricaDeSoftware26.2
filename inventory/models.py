from django.db import models
from django.conf import settings

class Product(models.Model):
    # Foreign key: every product is owned by a store (User)
    store = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    #MAIN
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=128, default='')
    brand = models.CharField(max_length=128, blank=True, default='')
    
    #ID
    sku = models.CharField(max_length=30, unique=True)
    bar_code = models.CharField(
        max_length=14,
        unique=True,
    )
    
    #STOCK & PRICE
    amount = models.PositiveBigIntegerField(default=0)
    low_stock_level = models.PositiveBigIntegerField(default=5)
    unitary_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    #AUDITING
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - [{self.sku}]"
    
    @property
    def is_low_stock(self):
        return self.amount <= self.low_stock_level