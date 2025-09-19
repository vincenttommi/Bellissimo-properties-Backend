from django.db import models
from users.models import User
from properties.models import ResidentialUnit
from bookings.models import AirbnbBooking


class Conversation(models.Model):
    TYPE_CHOICES = [
        ("residential", "Residential"),
        ("airbnb", "Airbnb"),
        ("general", "General"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    residential_unit = models.ForeignKey(ResidentialUnit, null=True, blank=True, on_delete=models.SET_NULL)
    airbnb_booking = models.ForeignKey(AirbnbBooking, null=True, blank=True, on_delete=models.SET_NULL)
  


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    attachments = models.TextField(blank=True, null=True)

