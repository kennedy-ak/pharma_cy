

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .utils import download_invoice

urlpatterns = [
    path('', views.home, name='home'),
        
    
    
    # Drug routes
    path('drugs/', views.drug_list, name='drug_list'),
    path('drugs/add/', views.add_drug, name='add_drug'),
    path('drugs/<int:pk>/edit/', views.edit_drug, name='edit_drug'),
    
    # Sale routes
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/invoice/', download_invoice, name='download_invoice'),
    
    # Reports
    path('reports/daily-sales/', views.daily_sales, name='daily_sales'),
    path('reports/monthly-sales/', views.monthly_sales, name='monthly_sales'),
    
    # Admin dashboard and analytics  
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('low-stock/', views.low_stock_report, name='low_stock_report'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # API endpoints
    path('api/search-drugs/', views.search_drugs, name='search_drugs'),
    path('api/drug-info/<int:drug_id>/', views.get_drug_info, name='get_drug_info'),
]