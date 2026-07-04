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
]