from django.db import models
from users.models import User
from properties.models import ResidentialUnit
from users.common import SoftDeletableModel, TimeStampedModel


class MaintenanceTicket(SoftDeletableModel, TimeStampedModel):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets_created",
        limit_choices_to={"role": "tenant"},
    )
    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets_managed",
        limit_choices_to={"role": "landlord"},
    )
    residential_unit = models.ForeignKey(ResidentialUnit, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    def __str__(self):
        return f"Ticket #{self.id} - {self.category} ({self.status})"
