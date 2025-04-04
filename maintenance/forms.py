from django import forms
from .models import MaintenanceRecord, MaintenanceSchedule
from expenses.models import Expense

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'vehicle', 'date', 'odometer', 'description', 'service_type', 
            'parts_used', 'labor_details', 'shop_name', 'shop_location', 
            'cost', 'expenses', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'parts_used': forms.Textarea(attrs={'rows': 3}),
            'labor_details': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'expenses': forms.SelectMultiple(attrs={'class': 'select2'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Set vehicle queryset
            self.fields['vehicle'].queryset = user.vehicle_set.all()
            self.fields['vehicle'].empty_label = "Select a vehicle"
            self.fields['vehicle'].required = True
            
        # If we already have a vehicle selected, filter expenses by that vehicle
        if self.instance and self.instance.vehicle_id:
            print(f"DEBUG: Form initialized with vehicle ID: {self.instance.vehicle_id}")
            self.fields['expenses'].queryset = Expense.objects.filter(
                vehicle=self.instance.vehicle
            ).order_by('-date')
        elif 'initial' in kwargs and 'vehicle' in kwargs['initial']:
            vehicle = kwargs['initial']['vehicle']
            print(f"DEBUG: Form initialized with initial vehicle: {vehicle.id}")
            self.fields['expenses'].queryset = Expense.objects.filter(
                vehicle=vehicle
            ).order_by('-date')
        else:
            print("DEBUG: Form initialized without vehicle")
            self.fields['expenses'].queryset = Expense.objects.none()
            
    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        
        if not vehicle:
            self.add_error('vehicle', 'A vehicle must be selected')
            
        return cleaned_data

class MaintenanceScheduleForm(forms.ModelForm):
    class Meta:
        model = MaintenanceSchedule
        fields = [
            'vehicle', 'name', 'description', 'interval_type', 
            'mileage_interval', 'time_interval_days', 
            'last_service_date', 'last_service_odometer', 'notes'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'last_service_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Set vehicle queryset
            self.fields['vehicle'].queryset = user.vehicle_set.all()
            self.fields['vehicle'].empty_label = "Select a vehicle"
            self.fields['vehicle'].required = True
            
        # Debug vehicle info for the instance
        if self.instance and self.instance.pk:
            print(f"DEBUG: Schedule form with instance vehicle: {self.instance.vehicle_id if self.instance.vehicle_id else 'None'}")
            
    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        
        if not vehicle:
            self.add_error('vehicle', 'A vehicle must be selected')
            
        return cleaned_data 