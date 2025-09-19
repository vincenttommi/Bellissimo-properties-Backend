import uuid
from django.db import models
from django.utils import timezone
from users.models import User
from properties.models import ResidentialUnit
from bookings.models import AirbnbBooking
from users.common import TimeStampedModel


class Payment(TimeStampedModel):
    METHOD_CHOICES = [
        ("mpesa", "M-Pesa"),
        ("bank", "Bank"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments_made"
    )
    landlord = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments_received"
    )
    residential_unit = models.ForeignKey(
        ResidentialUnit, null=True, blank=True, on_delete=models.SET_NULL
    )
    airbnb_booking = models.ForeignKey(
        AirbnbBooking, null=True, blank=True, on_delete=models.SET_NULL
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    transaction_reference = models.CharField(max_length=255, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    notified_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.payer} → {self.landlord} ({self.amount}) [{self.status}]"


class AppFeeConfig(TimeStampedModel):
    UNIT_CHOICES = [
        ("bedsitter", "Bedsitter"),
        ("1br", "1 Bedroom"),
        ("2br", "2 Bedroom"),
        ("airbnb", "Airbnb"),
    ]

    unit_type = models.CharField(max_length=20, choices=UNIT_CHOICES, unique=True)
    fixed_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.unit_type} Fee: {self.fixed_fee}"


class RevenueStream(TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    landlord = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "landlord"}
    )
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Revenue {self.fee_amount} from {self.landlord} [{self.status}]"


class PaymentType(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="payment_logos/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PaymentFieldConfig(TimeStampedModel):
    """
    Defines required fields for each PaymentType (e.g. Mpesa: phone_number, Bank: account_no)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_type = models.ForeignKey( PaymentType, on_delete=models.CASCADE, related_name="field_configs")
    field_name = models.CharField(max_length=100)
    field_label = models.CharField(max_length=100, blank=True, null=True)
    field_placeholder = models.CharField(max_length=100, blank=True, null=True)
    is_required = models.BooleanField(default=True)
    validation_regex = models.CharField(max_length=200, blank=True, null=True)
    validation_message = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ("payment_type", "field_name")

    def __str__(self):
        return f"{self.payment_type.name}: {self.field_name}"




class RentPaymentTransaction(TimeStampedModel):
    """
    Tracks landlord settlement of CR App fees
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    revenue_stream = models.ForeignKey(RevenueStream, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Settlement {self.amount_paid} for {self.revenue_stream}"



class PaymentMethod(TimeStampedModel):
    id = models.UUIDField(primary_key=True)
    payment_type = models.models(PaymentType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='payment_logos/', null=True, blank=True)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def get_field_configuration(self):
        config = {
            'required':[],
            'optional':[],
            'disallowed':[],
            'validation':{}
        }

        for field_config in self.field_configs.all():
            if field_config.is_required:
                config['required'].append(field_config.fieldd_name)
            elif field_config.is_allowed:
               config['optional'].append(field_config.field_name) 
            else:
                config['disallowed'].append(field_config.field_name)
            if field_config.validation_regex:
                config['validations'][field_config.field_name]={
                    'regex':field_config.validation_regex,
                    'message':field_config.validation_message or f"Invalid format for {field_config.field_name}"
                }               

        return  config



class PaymentDetails(TimeStampedModel):
    """
    Stores extra details for a Payment based on its PaymentMethod
    (e.g., Mpesa phone number, Bank account number, etc.)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="details"
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        related_name="payment_details"
    )

    details = models.JSONField(default=dict, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "payment_details"

    def __str__(self):
        return f"{self.payment_id} | {self.payment_method_id}"


