from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Vehicle(models.Model):
    TRANSMISSION_CHOICES = (
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('cvt', 'CVT'),
        ('dct', 'Dual-Clutch'),
        ('other', 'Other'),
    )
    
    # Basic Information
    nickname = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, blank=True, null=True, verbose_name="VIN")
    license_plate = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    mileage = models.IntegerField(default=0, help_text="Current vehicle mileage")
    
    # Vehicle specifications
    engine_type = models.CharField(max_length=100, blank=True, null=True)
    engine_displacement = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Engine size in liters")
    engine_power = models.IntegerField(blank=True, null=True, help_text="Power in hp/kW")
    transmission_type = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, blank=True, null=True)
    transmission_gears = models.IntegerField(blank=True, null=True)
    
    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.nickname})"
    
    def get_absolute_url(self):
        return reverse('vehicle-detail', kwargs={'pk': self.pk})
    
    @property
    def primary_image(self):
        """Return the primary image for this vehicle, or the first image if no primary is set."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image
        # If no primary image, return the first image
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return None


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_pics')
    is_primary = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.vehicle.nickname}"
    
    def save(self, *args, **kwargs):
        # If this is marked as primary, unmark others
        if self.is_primary:
            VehicleImage.objects.filter(vehicle=self.vehicle, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
