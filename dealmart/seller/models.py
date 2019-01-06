from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class OTP(models.Model):
    receiver = models.OneToOneField(User, on_delete = models.CASCADE)
    otp = models.IntegerField(null=False,blank=False)
    sent_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ("%s has received otps: %s" %(self.receiver.username,self.otp))
