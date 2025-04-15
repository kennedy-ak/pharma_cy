from django import forms
from .models import Drug, Sale, SaleItem, PaymentMethod

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'description', 'price', 'stock_quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['payment_method']

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