# from django.contrib import admin
# from .models import Drug, Sale, SaleItem, PaymentMethod

# class SaleItemInline(admin.TabularInline):
#     model = SaleItem
#     extra = 0

# @admin.register(Drug)
# class DrugAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'stock_quantity', 'updated_at')
#     search_fields = ['name', 'description']

# @admin.register(Sale)
# class SaleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'transaction_date', 'payment_method', 'total_amount')
#     inlines = [SaleItemInline]

# @admin.register(PaymentMethod)
# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ('name',)
from django.contrib import admin
from .models import Drug, Sale, SaleItem, PaymentMethod

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('get_total',)

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'updated_at')
    search_fields = ['name', 'description']
    list_filter = ('created_at', 'updated_at')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_date', 'payment_method', 'total_amount', 'created_at')
    inlines = [SaleItemInline]
    list_filter = ('transaction_date', 'payment_method', 'created_at')
    date_hierarchy = 'transaction_date'
    search_fields = ['id', 'payment_method__name']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']