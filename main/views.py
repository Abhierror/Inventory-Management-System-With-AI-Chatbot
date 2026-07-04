from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Sum, Q, F
from .models import (Category, Product, Supplier, Customer, StockTransaction,
                     Sale, SaleItem, AuditLog)
from .forms import (CategoryForm, ProductForm)

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
  
# Category 
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().order_by('name')
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs 
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx 
    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category 
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

    def from_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category Created Successfully.')
        return response 
    
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category 
    from_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        response = super.form_valid(form)
        messages.success(self.request, "Category Updated Successfully.")
        return response  
    
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category 
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        category_name = self.object.name
        messages.success(self.request, f'Category {category_name} Deleted Successfully.')
        return super().form_valid(form)

# Product
class ProductListView(LoginRequiredMixin, ListView):
    model = Product 
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().order_by('-created_by').select_related('category', 'supplier')
        q = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(sku__icontains=q))
        if category:
            qs = qs.filter(category_id=category)
        return qs 
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['categories'] = Category.objects.all()
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx 
    
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product 
    template_name = 'inventory/product_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_stock'] = self.object.get_current_stock() 
        ctx['is_low_stock'] = self.object.is_low_stock()
        ctx['transaction'] = self.object.stockTransaction_set_order_by('-created_by')[:10]
        return ctx 

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        response =  super().form_valid(form)
        messages.success(self.request, "Product Created Successfully")
        return response
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response =  super().form_valid(form)
        messages.success(self.request, "Product Updated Successfully")
        return response 
    
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product 
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product Deleted Successfully")
        return response
    