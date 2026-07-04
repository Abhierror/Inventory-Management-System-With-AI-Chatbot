from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 

    path('categories-list/', views.CategoryListView.as_view(), name="category_list"),
    path('categories/add/', views.CategoryCreateView.as_view(), name="category_add"),
    path('categories/<int:pk>/edit', views.CategoryUpdateView.as_view(), name="category_edit"),
    path('categories/<int:pk>/delete', views.CategoryDeleteView.as_view(), name="category_delete"), 

    path('products-list/', views.ProductListView.as_view(), name="product_list"),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name="product_edit"),
    path('products/add/', views.ProductCreateView.as_view(), name="product_add"),
    path('products/<int:pk>/edit', views.ProductUpdateView.as_view(), name="product_edit"),
    path('products/<int:pk>/delete', views.ProductDeleteView.as_view(), name="product_delete"), 
]