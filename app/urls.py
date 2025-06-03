# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
    
#     # Drug routes
#     path('drugs/', views.drug_list, name='drug_list'),
#     path('drugs/add/', views.add_drug, name='add_drug'),
#     path('drugs/<int:pk>/edit/', views.edit_drug, name='edit_drug'),
    
#     # Sale routes
#     path('sales/', views.sale_list, name='sale_list'),
#     path('sales/create/', views.create_sale, name='create_sale'),
#     path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    
#     # API endpoints
#     path('api/search-drugs/', views.search_drugs, name='search_drugs'),
#     path('api/drug-info/<int:drug_id>/', views.get_drug_info, name='get_drug_info'),
# ]


from django.urls import path
from . import views
from .utils import download_invoice

urlpatterns = [
    path('', views.home, name='home'),
         path('admin-login/', views.request_otp, name='request_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),
    
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
    
    # API endpoints
    path('api/search-drugs/', views.search_drugs, name='search_drugs'),
    path('api/drug-info/<int:drug_id>/', views.get_drug_info, name='get_drug_info'),
#    path('otp/request/', views.request_otp, name='request_otp'),
# path('otp/verify/', views.verify_otp, name='verify_otp'),

]