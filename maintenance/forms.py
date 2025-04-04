from django import forms
from .models import MaintenanceRecord, MaintenanceSchedule

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'vehicle', 'date', 'odometer', 'description', 'service_type', 
            'parts_used', 'labor_details', 'shop_name', 'shop_location', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'parts_used': forms.Textarea(attrs={'rows': 3}),
            'labor_details': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = user.vehicle_set.all()

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
            self.fields['vehicle'].queryset = user.vehicle_set.all() 