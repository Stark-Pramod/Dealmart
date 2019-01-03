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

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     first_name = models.CharField(max_length=10, blank=True,null=True,default='')
#     last_name = models.CharField(max_length=10, blank=True,null=True,default='')
#     # phone_number = PhoneNumberField(max_length=15, blank=True, null=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     avatar = models.ImageField(default='profile.png', upload_to='profile_pic')
#     GENDER_CHOICES=(
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Others', 'Others')
#     )
#     gender=models.CharField(max_length=10, choices=GENDER_CHOICES, default='')
#
#     def __str__(self):
        return self.user.username


