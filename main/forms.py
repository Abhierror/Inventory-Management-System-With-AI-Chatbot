from django import forms
from django.forms import formset_factory
from.models import Category, Supplier, Customer, Product, StockTransaction, Sale, SaleItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'row': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ["name", 'sku', 'category', 'supplier', 'cost_price', 'selling_price', 'reorder_level', 'product_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    