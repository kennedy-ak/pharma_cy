from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Drug, Sale, SaleItem, PaymentMethod
from .forms import DrugForm, SaleForm, SaleItemForm

from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from .models import Sale

def home(request):
    return render(request, 'app/home.html')

# Drug Management Views
def drug_list(request):
    drugs = Drug.objects.all().order_by('name')
    return render(request, 'app/drug_list.html', {'drugs': drugs})

def add_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug added successfully!')
            return redirect('drug_list')
    else:
        form = DrugForm()
    
    return render(request, 'app/add_drug.html', {'form': form})

def edit_drug(request, pk):
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

# Sales Views
def create_sale(request):
    payment_methods = PaymentMethod.objects.all()
    
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.total_amount = 0  # Will be updated later
            sale.save()
            
            # Process items from form data
            total = 0
            items = []
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
                
                items.append({
                    'drug': drug.name,
                    'quantity': quantity,
                    'price': price,
                    'total': price * quantity
                })
                
                i += 1
            
            # Update sale total
            sale.total_amount = total
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
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    
    return render(request, 'app/sale_detail.html', {
        'sale': sale,
        'items': items
    })

def sale_list(request):
    sales = Sale.objects.all().order_by('-transaction_date')
    return render(request, 'app/sale_list.html', {'sales': sales})

# AJAX Views
def search_drugs(request):
    query = request.GET.get('query', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    drugs = Drug.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).values('id', 'name', 'price', 'stock_quantity')
    
    return JsonResponse({'results': list(drugs)})

def get_drug_info(request, drug_id):
    drug = get_object_or_404(Drug, pk=drug_id)
    data = {
        'id': drug.id,
        'name': drug.name,
        'price': float(drug.price),
        'stock': drug.stock_quantity
    }
    return JsonResponse(data)




def daily_sales(request):
    """
    View to display daily sales statistics
    """
    # Group sales by date and calculate totals
    daily_stats = Sale.objects.annotate(
        date=TruncDate('transaction_date')
    ).values('date').annotate(
        total_sales=Sum('total_amount'),
        num_transactions=Count('id')
    ).order_by('-date')
    
    return render(request, 'app/daily_sales.html', {
        'daily_stats': daily_stats
    })

def monthly_sales(request):
    """
    View to display monthly sales statistics
    """
    from django.db.models.functions import TruncMonth
    
    # Group sales by month and calculate totals
    monthly_stats = Sale.objects.annotate(
        month=TruncMonth('transaction_date')
    ).values('month').annotate(
        total_sales=Sum('total_amount'),
        num_transactions=Count('id')
    ).order_by('-month')
    
    return render(request, 'app/monthly_sales.html', {
        'monthly_stats': monthly_stats
    })




