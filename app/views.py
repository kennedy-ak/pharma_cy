



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncDate, TruncMonth
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import requests

from .models import Drug, Sale, SaleItem, PaymentMethod, OTPVerification, AdminPhoneNumber, User
from .forms import DrugForm, SaleForm, SaleItemForm





# ========================
# AUTHENTICATION DECORATORS
# ========================

from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def admin_required(view_func):
    """Decorator to require admin role"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_admin():
            return HttpResponseForbidden("Admin access required")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def reception_or_admin_required(view_func):
    """Decorator for views accessible by both reception and admin"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_admin() or request.user.is_reception()):
            return HttpResponseForbidden("Access denied")
        return view_func(request, *args, **kwargs)
    return _wrapped_view




# ========================
# MAIN VIEWS
# ========================


# def home(request):
#     """Home view with authentication check"""
#     authenticated_phone = request.session.get('authenticated_phone', 'Unknown')
#     context = {
#         'authenticated_phone': authenticated_phone
#     }
#     return render(request, 'app/home.html', context)

def home(request):
    """Home view with role-based content"""
    from datetime import datetime
    from django.db import models
    
    # Calculate inventory statistics
    drugs = Drug.objects.all()
    total_drugs = drugs.count()
    
    # Calculate total inventory worth (price * stock_quantity for each drug)
    total_inventory_worth = 0
    for drug in drugs:
        total_inventory_worth += drug.price * drug.stock_quantity
    
    # Get recent sales count
    today = datetime.now().date()
    recent_sales_today = Sale.objects.filter(transaction_date__date=today).count()
    
    # Low stock count for admins
    low_stock_count = 0
    if request.user.is_authenticated and request.user.is_admin():
        low_stock_count = Drug.objects.filter(
            stock_quantity__lte=models.F('minimum_stock_level')
        ).count()
    
    context = {
        'total_drugs': total_drugs,
        'total_inventory_worth': total_inventory_worth,
        'recent_sales_today': recent_sales_today,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'app/home.html', context)

# ========================
# DRUG MANAGEMENT VIEWS
# ========================

@reception_or_admin_required
def drug_list(request):
    """Display list of all drugs"""
    drugs = Drug.objects.all().order_by('name')
    return render(request, 'app/drug_list.html', {'drugs': drugs})


@admin_required
def add_drug(request):
    """Add a new drug to inventory - Admin only"""
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug added successfully!')
            return redirect('drug_list')
    else:
        form = DrugForm()
    
    return render(request, 'app/add_drug.html', {'form': form})



@admin_required
def edit_drug(request, pk):
    """Edit an existing drug - Admin only"""
    drug = get_object_or_404(Drug, pk=pk)
    
    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug updated successfully!')
            return redirect('drug_list')
    else:
        form = DrugForm(instance=drug)
    
    return render(request, 'app/edit_drug.html', {'form': form, 'drug': drug})


# ========================
# SALES MANAGEMENT VIEWS
# ========================


@reception_or_admin_required
def create_sale(request):
    """Create a new sale transaction"""
    payment_methods = PaymentMethod.objects.all()
    
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.served_by = request.user
            sale.total_amount = 0  # Will be updated later
            sale.save()
            
            # Process items from form data
            total = 0
            i = 0
            while f'drug_{i}' in request.POST:
                drug_id = request.POST.get(f'drug_{i}')
                quantity = int(request.POST.get(f'quantity_{i}', 1))
                
                drug = Drug.objects.get(id=drug_id)
                price = drug.price
                
                # Create sale item
                sale_item = SaleItem(
                    sale=sale,
                    drug=drug,
                    quantity=quantity,
                    price_at_sale=price
                )
                sale_item.save()
                
                # Update total
                total += price * quantity
                
                # Reduce stock
                drug.stock_quantity -= quantity
                drug.save()
                
                i += 1
            
            # Update sale total and amount tendered
            sale.total_amount = total
            amount_tendered = request.POST.get('amount_tendered', 0)
            if amount_tendered:
                sale.amount_tendered = float(amount_tendered)
            sale.save()
            
            messages.success(request, 'Sale completed successfully!')
            return redirect('sale_detail', pk=sale.id)
    else:
        sale_form = SaleForm()
    
    context = {
        'sale_form': sale_form,
        'payment_methods': payment_methods,
        'item_form': SaleItemForm(),
    }
    return render(request, 'app/create_sale.html', context)



def sale_detail(request, pk):
    """Display details of a specific sale"""
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    
    return render(request, 'app/sale_detail.html', {
        'sale': sale,
        'items': items
    })



@admin_required
def sale_list(request):
    """Display list of all sales - Admin only"""
    sales = Sale.objects.all().order_by('-transaction_date')
    return render(request, 'app/sale_list.html', {'sales': sales})


# ========================
# REPORTING VIEWS
# ========================


@admin_required
def daily_sales(request):
    """Display daily sales statistics - Admin only"""
    daily_stats = Sale.objects.annotate(
        date=TruncDate('transaction_date')
    ).values('date').annotate(
        total_sales=Sum('total_amount'),
        num_transactions=Count('id')
    ).order_by('-date')
    
    return render(request, 'app/daily_sales.html', {
        'daily_stats': daily_stats
    })



@admin_required
def monthly_sales(request):
    """Display monthly sales statistics - Admin only"""
    monthly_stats = Sale.objects.annotate(
        month=TruncMonth('transaction_date')
    ).values('month').annotate(
        total_sales=Sum('total_amount'),
        num_transactions=Count('id')
    ).order_by('-month')
    
    return render(request, 'app/monthly_sales.html', {
        'monthly_stats': monthly_stats
    })


@admin_required
def admin_dashboard(request):
    """Admin dashboard with analytics and alerts"""
    from datetime import datetime, timedelta
    from django.db.models import Avg
    
    # Low stock alerts  
    from django.db import models
    low_stock_drugs = Drug.objects.filter(stock_quantity__lte=models.F('minimum_stock_level'))
    
    # Sales analytics
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    # Peak hours analysis
    hourly_sales = Sale.objects.values('hour_of_day').annotate(
        total_sales=Sum('total_amount'),
        avg_transaction_value=Avg('total_amount')
    ).order_by('hour_of_day')
    
    # Day of week analysis  
    weekly_sales = Sale.objects.values('day_of_week').annotate(
        total_sales=Sum('total_amount'),
        transaction_count=Count('id')
    ).order_by('day_of_week')
    
    # Top selling drugs
    top_drugs = SaleItem.objects.values('drug__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(models.F('quantity') * models.F('price_at_sale'))
    ).order_by('-total_quantity')[:10]
    
    # Recent sales
    recent_sales = Sale.objects.filter(
        transaction_date__date=today
    ).select_related('served_by').order_by('-transaction_date')[:10]
    
    context = {
        'low_stock_drugs': low_stock_drugs,
        'hourly_sales': hourly_sales,
        'weekly_sales': weekly_sales,
        'top_drugs': top_drugs,
        'recent_sales': recent_sales,
        'low_stock_count': low_stock_drugs.count(),
    }
    
    return render(request, 'app/admin_dashboard.html', context)


@admin_required  
def low_stock_report(request):
    """Detailed low stock report"""
    from django.db import models
    low_stock_drugs = Drug.objects.filter(
        stock_quantity__lte=models.F('minimum_stock_level')
    ).order_by('stock_quantity')
    
    return render(request, 'app/low_stock_report.html', {
        'low_stock_drugs': low_stock_drugs
    })


# ========================
# AJAX/API VIEWS
# ========================

@reception_or_admin_required
def search_drugs(request):
    """AJAX endpoint for drug search"""
    query = request.GET.get('query', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    drugs = Drug.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).values('id', 'name', 'price', 'stock_quantity')
    
    return JsonResponse({'results': list(drugs)})



def get_drug_info(request, drug_id):
    """AJAX endpoint to get drug information"""
    drug = get_object_or_404(Drug, pk=drug_id)
    data = {
        'id': drug.id,
        'name': drug.name,
        'price': float(drug.price),
        'stock': drug.stock_quantity
    }
    return JsonResponse(data)


def custom_logout(request):
    """Custom logout view with message"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')




