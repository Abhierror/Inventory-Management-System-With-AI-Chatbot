from django import forms
from django.forms import formset_factory
from.models import Category, Supplier, Customer, Product, StockTransaction, Sale, SaleItem

class CategoryForm(forms.ModelForm):
    class meta:
        model = Category 
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'row': 3}),
        }


    