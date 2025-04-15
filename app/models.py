

# Create your models here.
from django.db import models
from django.utils import timezone

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