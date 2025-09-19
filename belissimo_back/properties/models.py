from django.db import models
from users.models import User
from users.common import SoftDeletableModel, TimeStampedModel
from  properties.models import Property

class Property(SoftDeletableModel, TimeStampedModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("full", "Full"),
    ]
    name = models.CharField(max_length=255)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "landlord"})
    location = models.TextField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    def __str__(self):
        return f"{self.name} ({self.status})"


class ResidentialUnit(SoftDeletableModel, TimeStampedModel):
    UNIT_CHOICES = [
        ("bedsitter", "Bedsitter"),
        ("1br", "1 Bedroom"),
        ("2br", "2 Bedroom"),
    ]

    STATUS_CHOICES = [
        ("vacant", "Vacant"),
        ("occupied", "Occupied"),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=20, choices=UNIT_CHOICES)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenant = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"role": "tenant"},
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="vacant")

    def __str__(self):
        return f"{self.property.name} - Unit {self.unit_number} ({self.status})"
