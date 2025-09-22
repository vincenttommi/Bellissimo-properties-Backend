from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from . common import SoftDeletableModel, TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model for Bellissimo app.
    - Email is required to send password reset links when admins create users.
    - Passwords are not set during creation; instead, a reset token is generated,
      and an email is sent to the user with a link to set their password.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True, null=False, blank=False)  
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    government_id = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=50, blank=True, null=True) 
    refund_details = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.username} ({self.role})"


class Property(SoftDeletableModel, TimeStampedModel):
    TYPE_CHOICES = (
        ('rental', 'Rental Apartment'),
        ('sale', 'For Sale'),
        ('airbnb', 'Airbnb'),
        ('construction', 'Construction Project'),
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rooms = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    landlord = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'landlord'}, related_name='owned_properties'
    )
    admin_posted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='posted_properties', limit_choices_to={'role': 'admin'}
    )
    is_available = models.BooleanField(default=True)  
    photos = models.JSONField(default=list, blank=True)  

    def __str__(self):
        return f"{self.name} ({self.property_type})"


class TenantAssignment(SoftDeletableModel, TimeStampedModel):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    property = models.ForeignKey(Property, on_delete=models.CASCADE, limit_choices_to={'property_type': 'rental'})
    move_in_date = models.DateField(blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=15, decimal_places=2)
    rent_due_date = models.DateField() 

    class Meta:
        unique_together = ('tenant', 'property')

    def __str__(self):
        return f"{self.tenant} in {self.property}"


class MaintenanceTicket(TimeStampedModel):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )
    TYPE_CHOICES = (
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('installations', 'Installations'),
        ('other', 'Other'),
    )
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    property = models.ForeignKey(Property, on_delete=models.CASCADE, limit_choices_to={'property_type': 'rental'})
    ticket_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_professional = models.ForeignKey('MaintenanceProfessional', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.id} by {self.tenant} for {self.property}"


class Payment(TimeStampedModel):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    property = models.ForeignKey(Property, on_delete=models.CASCADE, limit_choices_to={'property_type': 'rental'})
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=(('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue')),
        default='pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    cr_app_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Payment {self.id} by {self.tenant} for {self.property}"


class VirtualWallet(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet for {self.user}"


class WalletTransaction(TimeStampedModel):
    TYPE_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('rent_payment', 'Rent Payment'),
        ('token_purchase', 'Token Purchase'),
        ('referral_bonus', 'Referral Bonus'),
        ('reward', 'Reward'),
    )
    wallet = models.ForeignKey(VirtualWallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction {self.id} for {self.wallet.user}"


class ElectricityToken(TimeStampedModel):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    property = models.ForeignKey(Property, on_delete=models.CASCADE, limit_choices_to={'property_type': 'rental'})
    token_code = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token_code} for {self.tenant}"


class ChatMessage(TimeStampedModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class Referral(TimeStampedModel):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received')
    bonus_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Referral from {self.referrer} to {self.referred}"


class MaintenanceProfessional(TimeStampedModel):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)  
    phone_number = models.CharField(max_length=20)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  

    def __str__(self):
        return f"{self.name} ({self.specialty})"


class EmergencyContact(TimeStampedModel):
    TYPE_CHOICES = (
        ('police', 'Police'),
        ('fire', 'Fire'),
    )
    contact_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.contact_type} Contact"
