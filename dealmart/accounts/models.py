# from django.db import models
from djongo import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Role(models.Model):
    """
    this is defined to allot a role to a user.
    """

    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return '%s'%(self.role)


class User(AbstractUser):
    """
    user is customised and related to model Role using Abstract user.
    """
    roles = models.ManyToManyField(Role)


class OTP(models.Model):
    """
    Model to store Otp of user And verify user.
    """
    receiver = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=False,blank=False)
    sent_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ("%s has received otps: %s" %(self.receiver.username,self.otp))


class DeliveryAddress(models.Model):
    """
    Model to store delivery Address of buyer.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20, blank=False,null=False)
    pin_code = models.CharField(max_length=6, blank=False,null=False)
    phone_number = PhoneNumberField(max_length=13,blank=False,null=False)
    residence = models.CharField(max_length=50,blank=False,null=False)
    locality = models.CharField(max_length=60,blank=False,null=False)
    landmark = models.CharField(max_length=50,blank=True,null=True,default='')
    district  = models.CharField(max_length=50,blank=False,null=False)
    city = models.CharField(max_length=20,blank=False,null=False)
    STATE_CHOICES =(
        ('Uttar Pradesh','Uttar Pradesh'),
        ('Delhi','Delhi'),
        ('Punjab','Punjab')
    )
    state = models.CharField(max_length=30,choices=STATE_CHOICES,default='',null=False,blank=False)
    COUNTRY_CHOICES = (
        ('India','India'),
    )
    country = models.CharField(max_length=15, choices=COUNTRY_CHOICES, default='India')

    def __str__(self):
        return "% has delivery address %s"%(self.user.username,self.city)


class PickupAddress(models.Model):
    """
    model to store Pickup address of seller.
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Company_name = models.CharField(max_length=50, blank=False,null=False)
    pin_code = models.CharField(max_length=6, blank=False,null=False)
    phone_number = PhoneNumberField(max_length=13,blank=False,null=False)
    full_address = models.CharField(max_length=100,blank=False,null=False)
    city = models.CharField(max_length=20,blank=False,null=False)
    STATE_CHOICES =(
         ('Uttar Pradesh','Uttar Pradesh'),
         ('Delhi','Delhi'),
         ('Punjab','Punjab')
     )
    state = models.CharField(max_length=30,choices=STATE_CHOICES,default='',null=False,blank=False)
    COUNTRY_CHOICES = (
        ('India','India'),
      )
    country = models.CharField(max_length=15, choices=COUNTRY_CHOICES, default='India')

    def __str__(self):
        return "% has pickup address %s"%(self.Company_name,self.city)


class SellerDetails(models.Model):
    """
    model to store bank details and other tax related details of seller.
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20, blank=False,null=False)
    bank_account_no = models.BigIntegerField(blank=False,null=False)
    IFSC_code = models.CharField(max_length=11,blank=False,null=False)
    aadhar_no = models.BigIntegerField(blank=False,null=True)
    pan_card_no = models.CharField(max_length=10,blank=True,null=False)

    def __str__(self):
        return (self.user.username)

class Category(models.Model):
    category = models.CharField(max_length=30,null=True,blank=False)

    def __str__(self):
        return "%s"%(self.category)


class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=30,null=False,blank=False)

    def __str__(self):
        return "%s"%(self.subcategory)



class Product(models.Model):
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    subcategory = models.OneToOneField(Subcategory,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=15,null=False,blank=False)
    image = models.ImageField(default='product_pics/download.png',null=False,blank=False,upload_to='product_pics')
    video = models.FileField(upload_to ='product_videos', null=True, blank=True)
    # CAT_CH = (
    #     ('electronics','Electronics'),
    #     ('mobile','Mobile'),
    #     ('laptop','Laptop'),
    #     ('men','Men'),
    #     ('women','Women'),
    #     ('kids','Kids'),
    #     ('groceries','Groceries'),
    #     ('cosmetics','Cosmetics'),
    #     ('footwear','Footwear'),
    #     ('sports','Sports'),
    #     ('books','Books'),
    #     ('furnitures','Furnitures'),
    #     ('decorations','Decorations'),
    # )
    # category = models.CharField(choices=CAT_CH,max_length=20,blank=True)


    def __str__(self):
        return "%s is of %s"%(self.name,self.user.username)


