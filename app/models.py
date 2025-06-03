

# Create your models here.
from django.db import models
from django.utils import timezone
import random


class Drug(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    transaction_date = models.DateTimeField(default=timezone.now)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    
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