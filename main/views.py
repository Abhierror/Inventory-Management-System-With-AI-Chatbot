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
            
# Dashboard 
@login_required
def dashboard(request):
    total_products = Product.objects.count()
    low_stock_products = [p for p in Product.objects.all() if p.is_low_stock()]
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    recent_transactions = StockTransaction.objects.select_related('product', 'created_at').order_by('-created_at')[:10]
    recent_sales = Sale.objects.select_related('customer', 'created_at').order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'low_stock_count': len(low_stock_products),
        'low_stock_products': low_stock_products[:5],
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'recent_transactions': recent_transactions,
        'recent_sales': recent_sales
    }

    return render(request, 'inventory/dashboard.html', context)
  
