from django.db import models
from django.urls import reverse
from vehicles.models import Vehicle
from django.utils import timezone
from expenses.models import Expense

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateField()
    odometer = models.IntegerField(help_text="Odometer reading at time of service")
    description = models.CharField(max_length=255)
    service_type = models.CharField(max_length=100)
    parts_used = models.TextField(blank=True, null=True)
    labor_details = models.TextField(blank=True, null=True)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    shop_location = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    expenses = models.ManyToManyField(Expense, blank=True, related_name='maintenance_records')
    
    def __str__(self):
        return f"{self.service_type} - {self.date}"
    
    def get_absolute_url(self):
        return reverse('maintenance-record-detail', kwargs={'pk': self.pk})

class MaintenanceSchedule(models.Model):
    INTERVAL_TYPE_CHOICES = (
        ('mileage', 'Mileage'),
        ('date', 'Date'),
        ('both', 'Mileage and Date'),
    )
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_schedules')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    interval_type = models.CharField(max_length=10, choices=INTERVAL_TYPE_CHOICES)
    mileage_interval = models.IntegerField(blank=True, null=True, help_text="Mileage interval between services")
    time_interval_days = models.IntegerField(blank=True, null=True, help_text="Days between services")
    last_service_date = models.DateField(blank=True, null=True)
    last_service_odometer = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.vehicle:
            return f"{self.name} for {self.vehicle.nickname}"
        return f"{self.name} (No vehicle assigned)"
    
    def get_absolute_url(self):
        return reverse('maintenance-schedule-detail', kwargs={'pk': self.pk})
    
    @property
    def next_service_date(self):
        if self.interval_type in ['date', 'both'] and self.last_service_date and self.time_interval_days:
            return self.last_service_date + timezone.timedelta(days=self.time_interval_days)
        return None
    
    @property
    def next_service_mileage(self):
        if self.interval_type in ['mileage', 'both'] and self.last_service_odometer and self.mileage_interval:
            return self.last_service_odometer + self.mileage_interval
        return None
    
    @property
    def is_due(self):
        today = timezone.now().date()
        if self.interval_type == 'date' and self.next_service_date:
            return self.next_service_date <= today
        elif self.interval_type == 'mileage':
            # Assuming we'd check this against current mileage in a view
            return False
        elif self.interval_type == 'both':
            date_due = self.next_service_date and self.next_service_date <= today
            # For mileage, we'll need to check this in a view
            return date_due
        return False
