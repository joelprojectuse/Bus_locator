# Generated by Django 4.2.3 on 2024-01-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bus_final', '0004_customuser_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverlocation',
            name='id',
        ),
        migrations.AlterField(
            model_name='driverlocation',
            name='driver_number',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
