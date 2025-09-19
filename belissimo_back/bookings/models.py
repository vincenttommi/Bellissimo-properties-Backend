from django.db import models
from users.models import User
from properties.models import Property
from users.common import SoftDeletableModel, TimeStampedModel


class AirbnbUnit(SoftDeletableModel,TimeStampedModel):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
        ("inactive", "Inactive"),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    landlord = models.ForeignKey( User, on_delete=models.CASCADE, limit_choices_to={"role": "landlord"})
    title = models.CharField(max_length=255) 
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2) 
    max_guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"{self.title} ({self.status})"


class AirbnbBooking(SoftDeletableModel,TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    airbnb_unit = models.ForeignKey(AirbnbUnit, on_delete=models.CASCADE)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "landlord"})
    guest_name = models.CharField(max_length=255)
    guest_phone = models.CharField(max_length=50)
    check_in = models.DateField()
    check_out = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Booking for {self.guest_name} ({self.status})"
