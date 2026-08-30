from django import forms
from .models import Product, Sale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'brand', 'sku',
            'bar_code', 'amount', 'low_stock_level', 'unitary_price'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Digite o nome do produto'}),
            'description': forms.Textarea(attrs={'placeholder': 'Adicione uma descrição ao produto'}),
            'category': forms.TextInput(attrs={'placeholder': 'Digite a categoria do produto'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Digite a marca do produto'}),
            'sku': forms.TextInput(attrs={'placeholder': 'Digite a sku do produto'}),
            'bar_code': forms.TextInput(attrs={'placeholder': 'Digite o código de barras do produto'}),
            'amount': forms.NumberInput(attrs={'min': '1'}),
            'low_stock_level': forms.NumberInput(attrs={'min': '1'}),
            'unitary_price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'category': 'Categoria',
            'brand': 'Marca',
            'sku': 'SKU',
            'bar_code': 'Código de barras',
            'amount': 'Quantidade',
            'low_stock_level': 'Estoque mínimo',
            'unitary_price': 'Valor unitário',
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'buyer_name', 'quantity_sold']
        widgets = {
            'buyer_name': forms.TextInput(attrs={'placeholder': 'Nome do cliente (opcional)'}),
            'quantity_sold': forms.NumberInput(attrs={'min': '1', 'value': '1'}),
        }
        labels = {
            'product': 'Produto',
            'buyer_name': 'Cliente',
            'quantity_sold': 'Quantidade',
        }

    def __init__(self, *args, **kwargs):
        # Captures the user before the form starts
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filters the dropdown: only the shopkeeper's products with available stock
            self.fields['product'].queryset = Product.objects.filter(store=user, amount__gt=0)
            self.fields['product'].empty_label = "> SELECIONE_O_ITEM..."