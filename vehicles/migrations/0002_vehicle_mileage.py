# Generated by Django 5.2 on 2025-04-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='mileage',
            field=models.IntegerField(default=0, help_text='Current vehicle mileage'),
        ),
    ]
