from django.db import models


class EmergencyContact(models.Model):
    TYPE_CHOICES = [("police", "Police"), ("fire", "Fire"), ("askari", "Askari")]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    phone_number = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class Ad(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    title = models.CharField(max_length=255)
    image = models.TextField()
    link = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
