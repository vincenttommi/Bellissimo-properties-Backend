from django.db import models
from users.models import User
from properties.models import ResidentialUnit


class MaintenanceTicket(models.Model):
    STATUS_CHOICES = [("open", "Open"), ("in_progress", "In Progress"), ("resolved", "Resolved")]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets_created")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets_managed")
    residential_unit = models.ForeignKey(ResidentialUnit, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
 
