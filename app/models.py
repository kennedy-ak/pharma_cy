

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):
    """Custom User model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('reception', 'Reception'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reception')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(null=True, blank=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_reception(self):
        return self.role == 'reception'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Drug(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    minimum_stock_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.stock_quantity <= self.minimum_stock_level

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    # Basic transaction info
    transaction_date = models.DateTimeField(default=timezone.now)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_tendered = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    # Enhanced data collection
    served_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_served')
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)

    # Transaction metadata
    day_of_week = models.CharField(max_length=10, blank=True)  # Monday, Tuesday, etc.
    hour_of_day = models.IntegerField(null=True, blank=True)  # 0-23
    is_weekend = models.BooleanField(default=False)

    # Additional notes
    notes = models.TextField(blank=True, null=True)
    discount_applied = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Percentage
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Auto-populate analytics data
        if self.transaction_date:
            self.day_of_week = self.transaction_date.strftime('%A')
            self.hour_of_day = self.transaction_date.hour
            self.is_weekend = self.transaction_date.weekday() >= 5
        super().save(*args, **kwargs)

    def get_change(self):
        """Calculate change amount"""
        from decimal import Decimal
        total_with_tax = self.total_amount * Decimal('1.09')  # 9% total tax
        return max(self.amount_tendered - total_with_tax, Decimal('0.00'))
    
    def __str__(self):
        return f"Sale #{self.id} - {self.transaction_date.strftime('%Y-%m-%d %H:%M')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.drug.name} - {self.quantity} units"
    
    def get_total(self):
        return self.price_at_sale * self.quantity
    


class DailySalesSummary(models.Model):
    date = models.DateField(unique=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    num_transactions = models.IntegerField(default=0)

    def __str__(self):
        return f"Daily Summary for {self.date}"
    
class MonthlySalesSummary(models.Model):
    month = models.DateField(unique=True)  # store the first day of the month
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    num_transactions = models.IntegerField(default=0)

    def __str__(self):
        return f"Monthly Summary for {self.month.strftime('%B %Y')}"
    




# class OTPVerification(models.Model):
#     phone_number = models.CharField(max_length=15)
#     otp_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_verified = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if not self.otp_code:
#             self.otp_code = f"{random.randint(100000, 999999)}"
#         super().save(*args, **kwargs)

from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(minutes=10)

class AdminPhoneNumber(models.Model):
    """Model to store admin phone numbers for OTP verification"""
    phone_number = models.CharField(max_length=15, unique=True,default="0557782728")
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=100, blank=True, help_text="Description of who this number belongs to")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone_number} - {self.description}"
    
    class Meta:
        verbose_name = "Admin Phone Number"
        verbose_name_plural = "Admin Phone Numbers"

class OTPVerification(models.Model):
    admin_phone = models.ForeignKey(AdminPhoneNumber, on_delete=models.CASCADE,default=1)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
 
    expires_at = models.DateTimeField(default=default_expiry)
    
    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = f"{random.randint(100000, 999999)}"
        
        # Set expiration time (10 minutes from creation)
        if not self.expires_at:
            from django.utils import timezone
            from datetime import timedelta
            self.expires_at = timezone.now() + timedelta(minutes=10)
            
        super().save(*args, **kwargs)
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.admin_phone.phone_number} - {self.otp_code}"
    
    class Meta:
        verbose_name = "OTP Verification"
        verbose_name_plural = "OTP Verifications"