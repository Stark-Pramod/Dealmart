from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Role(models.Model):
    BUYER = 1
    SELLER = 2
    ROLE_CHOICES = (
        (BUYER, 'buyer'),
        (SELLER, 'seller'),
        )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
         return self.get_id_display()

class User(AbstractUser):
    roles = models.ManyToManyField(Role)


class OTP(models.Model):
    receiver = models.OneToOneField(User, on_delete = models.CASCADE)
    otp = models.IntegerField(null=False,blank=False)
    sent_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ("%s has received otps: %s" %(self.receiver.username,self.otp))


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20, blank=False,null=False)
    pin_code = models.CharField(max_length=10, blank=False,null=False)
    phone_number = PhoneNumberField(max_length=13,blank=False,null=False)
    residence = models.CharField(max_length=50,blank=False,null=False)
    locality = models.CharField(max_length=60,blank=False,null=False)
    landmark = models.CharField(max_length=50,blank=True,null=True,default='')
    city = models.CharField(max_length=20,blank=False,null=False)

    def __str__(self):
        return ("% has dilivery address %s"%(self.user.username,self.city))

