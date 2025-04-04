from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

# Create your models here.

class Profile(models.Model):
    UNIT_CHOICES = (
        ('metric', 'Metric (km, liters)'),
        ('imperial', 'Imperial (miles, gallons)'),
    )
    
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('HUF', 'Hungarian Forint (Ft)'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    unit_system = models.CharField(max_length=10, choices=UNIT_CHOICES, default='metric')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    receive_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Check if the image file exists
        try:
            if os.path.exists(self.image.path):
                img = Image.open(self.image.path)
                
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
        except (IOError, SyntaxError, ValueError) as e:
            # Handle invalid or corrupted image file
            print(f"Error processing image: {e}")
            # The user can upload a new image later
