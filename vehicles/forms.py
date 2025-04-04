from django import forms
from .models import Vehicle, VehicleImage

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'nickname', 'make', 'model', 'year', 'vin', 'license_plate', 
            'description', 'engine_type', 'engine_displacement', 'engine_power',
            'transmission_type', 'transmission_gears', 'mileage'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image', 'description', 'is_primary'] 