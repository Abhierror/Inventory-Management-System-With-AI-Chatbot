from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import (Category, Product, Supplier, Customer, StockTransaction,
                     Sale, SaleItem, AuditLog)

# Authentication 
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form =  AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/login.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
            
