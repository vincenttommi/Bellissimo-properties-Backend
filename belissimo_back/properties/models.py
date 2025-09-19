from django.db import models
from users.models import User


class  Property(models.Model):
    STATUS_CHOICES = [
        ("active","Active"),
        ("inactive","Inactive"),
        ("full","Full"),
    ]


    landlord =  models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role":"landlord"})
    name = models.CharField(max_length=255)
    location = models.TextField()
    description = models.TextField(blank=True)
    status  = models.DateTimeField(auto_now_add=True)
     



class ResidentialUnit(models.Model):
    UNIT_CHOICES = [
        ("bedsitter","Bedsitter"),
        ("1br","1 Bedroom"),
        ("2br","2 Bedroom"),
    ]     


    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    rent_amount = models.DecimalField(max_digits=10,decimal_places=2)
    tenant = models.ForeignKey(User, null=True, blank=True,on_delete=models.SET_NULL,limit_choices_to={"role":"tenant"})
    status = models.CharField(max_length=20,choices=[("vacant","Vacant"),("occuppied","Occuppied")],default="vacant")








