from django import forms
from .models import Drug, Sale, SaleItem, PaymentMethod

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'description', 'price', 'stock_quantity', 'minimum_stock_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SaleForm(forms.ModelForm):
    amount_tendered = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        label="Amount Tendered",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'step': '0.01',
            'placeholder': 'Enter amount tendered'
        }),
        help_text="Required for cash payments"
    )
    
    class Meta:
        model = Sale
        fields = ['payment_method', 'amount_tendered']

class SaleItemForm(forms.ModelForm):
    drug_search = forms.CharField(
        label="Search Drug",
        required=False,
        widget=forms.TextInput(attrs={'class': 'drug-search', 'autocomplete': 'off'})
    )
    
    class Meta:
        model = SaleItem
        fields = ['drug', 'quantity']
        widgets = {
            'drug': forms.HiddenInput(),
        }

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name']

