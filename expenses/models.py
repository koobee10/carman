from django.db import models
from django.urls import reverse
from vehicles.models import Vehicle

class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('parts', 'Parts'),
        ('service', 'Service'),
        ('fluids', 'Fluids'),
        ('tools', 'Tools'),
        ('accessories', 'Accessories'),
        ('other', 'Other'),
    )
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    vendor_location = models.CharField(max_length=255, blank=True, null=True)
    vendor_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_cost(self):
        return self.amount + self.tax + self.shipping + self.labor_cost
    
    def __str__(self):
        return f"{self.description} - {self.date}"
    
    def get_absolute_url(self):
        return reverse('expense-detail', kwargs={'pk': self.pk})

class Receipt(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='receipts')
    image = models.ImageField(upload_to='receipts')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Receipt for {self.expense.description}"
