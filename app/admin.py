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
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Drug, Sale, SaleItem, PaymentMethod, AdminPhoneNumber, OTPVerification, User

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('get_total',)

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'minimum_stock_level', 'is_low_stock', 'updated_at')
    search_fields = ['name', 'description']
    list_filter = ('created_at', 'updated_at')
    
    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_date', 'served_by', 'payment_method', 'total_amount', 'day_of_week', 'created_at')
    inlines = [SaleItemInline]
    list_filter = ('transaction_date', 'payment_method', 'served_by', 'day_of_week', 'is_weekend', 'created_at')
    date_hierarchy = 'transaction_date'
    search_fields = ['id', 'payment_method__name', 'served_by__username', 'customer_name']
    
    fieldsets = (
        ('Transaction Info', {
            'fields': ('transaction_date', 'payment_method', 'total_amount', 'amount_tendered')
        }),
        ('Staff & Customer', {
            'fields': ('served_by', 'customer_name', 'customer_phone', 'customer_email')
        }),
        ('Analytics Data', {
            'fields': ('day_of_week', 'hour_of_day', 'is_weekend', 'discount_applied', 'tax_amount'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

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


# Custom User Admin
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phone_number', 'is_active', 'is_staff')

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = ('username', 'email', 'role', 'phone_number', 'is_active', 'is_staff', 'last_login')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_login_time')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'phone_number', 'password1', 'password2'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined', 'last_login_time')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new user
            # Set default permissions based on role
            if obj.role == 'admin':
                obj.is_staff = True
            else:
                obj.is_staff = False
        super().save_model(request, obj, form, change)