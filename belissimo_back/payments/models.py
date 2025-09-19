from django.db import models
from users.models import User
from properties.models import ResidentialUnit
from bookings.models import AirbnbBooking




class Payment(models.Model):
    METHOD_CHOICES = [("mpesa","M-pesa"),("bank","Bank")]
    STATUS_CHOICES = [("pending"),"Pending",("completed","Completed"),("failed","Failed")]
    

    payer =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_made")
    landlord =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_recieved")
    residential_unit = models.ForeignKey(ResidentialUnit, null=True, blank=True,on_delete=models.SET_NULL)
    airbnb_booking = models.ForeignKey(AirbnbBooking, null=True, blank=True, on_delete=models.SET_NULL)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)
    method =  models.CharField(max_length=20, choices=METHOD_CHOICES)
    status =  models.CharField(max_length=255, blank=True)
    transaction_reference = models.CharField(max_length=255, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    notified_admin =  models.BooleanField(default=True)




class  AppFeeConfig(models.Model):
    UNIT_CHOICES = [
        ("bedsitter","Bedsitter"),
        ("1br","1 Bedroom"),
        ("2br","2 Bedroom"),
        ("airbnb","Airbnb"),
    ]

    unit_type = models.CharField(max_length=20, choices=UNIT_CHOICES)
    fixed_fee =  models.DecimalField(max_digits=10, decimal_places=2)

    



class RevenueStream(models.Model):
    STATUS_CHOICES = [("pending","Pending"),("paid","Paid")]

    payment =  models.ForeignKey(Payment, on_delete=models.CASCADE)
    landlord =  models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={"role":"landlord"})
    fee_amount =  models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

