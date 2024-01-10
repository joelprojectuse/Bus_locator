from django.db import models
from django_jsonform.models.fields import ArrayField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


ROLE_CHOICES = (
    ("driver", "Driver"),
    ("conductor", "Conductor"),
)
SECTOR_CHOICES = (
    ("government", "Government"),
    ("private", "Private"),
)


class CustomUser(AbstractUser):
    Name = models.CharField(max_length=50, null=False, blank=False)
    DOB = models.DateField(null=True)
    # Allow null values for DOB
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits is allowed.")
    )

    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        null=True,
        blank=True,
        unique=True
    )

    role = models.CharField(
        max_length=15, choices=ROLE_CHOICES, default='driver')
    sector = models.CharField(
        max_length=15, choices=SECTOR_CHOICES, default='private')
    depo = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.username


class Route(models.Model):
    route_name = models.CharField(max_length=10, null=False, blank=False)
    route_List = ArrayField(
        models.CharField(max_length=35, blank=True),
        size=50
    )

    def __str__(self):
        return self.route_name


class DriverLocation(models.Model):
    route_number = models.CharField(max_length=10, null=False, blank=False)
    driver_number = models.CharField(
        primary_key=True, max_length=50, null=False, blank=False)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    created_by = models.ForeignKey(
        'app_bus_final.CustomUser', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.driver_number
