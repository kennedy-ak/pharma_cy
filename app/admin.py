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
from .models import Drug, Sale, SaleItem, PaymentMethod, AdminPhoneNumber, OTPVerification

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




@admin.register(AdminPhoneNumber)
class AdminPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('phone_number', 'description')
    list_editable = ('is_active',)
    
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'description', 'is_active')
        }),
    )

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('admin_phone', 'otp_code', 'is_verified', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('is_verified', 'created_at', 'admin_phone')
    search_fields = ('admin_phone__phone_number', 'otp_code')
    readonly_fields = ('otp_code', 'created_at', 'expires_at')
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'