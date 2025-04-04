from django import forms
from .models import Expense, Receipt

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'vehicle', 'date', 'description', 'category', 'amount', 
            'tax', 'shipping', 'labor_cost', 'vendor', 'vendor_location', 
            'vendor_url', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = user.vehicle_set.all()

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['image'] 