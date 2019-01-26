# from django.db import models
from djongo import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Role(models.Model):
    """
    this is defined to allot a role to a user.
    """
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
    """
    user is customised and related to model Role using Abstract user.
    """
    roles = models.ManyToManyField(Role)


class OTP(models.Model):
    """
    Model to store Otp of user And verify user.
    """
    receiver = models.OneToOneField(User, on_delete = models.CASCADE)
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

class Subcategory(models.Model):
    # product = models.OneToOneField(Product,on_delete=models.CASCADE)
    ELEC_CH =(
        ('mobile','Mobile'),
        ('Laptop','Laptop'),
        ('earphone','Earphone'),
        ('speaker','Speaker'),
        ('air_conditioner','Air Conditioner'),
        ('washing_machine','Washing Machine'),
        ('water_pump','Water Pump'),
        ('hair_drier','Hair Drier'),
        ('projector','Projector'),
        ('desktop','Desktop'),
        ('cpu','CPU'),
        ('mouse','Mouse'),
        ('keyboard','Keyboard'),
        ('other','Other')
    )
    DEC_CH= (
        ('vase','Vase'),
        ('painting','Painting'),
        ('statue','Statue'),
        ('curtain','Curtain'),
        ('bedsheet','Bedsheet'),
    )
    MEN_WEAR_CH =(
        ('shirt','Shirt'),
        ('t-shirt','T-shirt'),
        ('jeans','Jeans'),
        ('pant','Pant'),
        ('trouser','Trouser'),
        ('jacket','Jacket'),
        ('suit','Suit')
    )
    WOMEN_WEAR_CH = (
        ('top','Top'),
        ('jeans','Jeans'),
        ('saari','Saari'),
        ('lehnga','Lehnga'),
        ('t-shirt','T-shirt'),
        ('suit','Suit'),
        ('salwar','Salwar'),
    )
    KIDS_CH = (
        ('cap','Cap'),
        ('shirt','Shirt'),
        ('inner_wear','Inner Wear'),
        ('diaper','Diaper'),
        ('t-shirt','T-shirt'),
        ('half-pant','Half Pant'),
        ('full-pant','Full Pant'),
        ('bottle','Bottle')
    )

    electronics = models.CharField(choices=ELEC_CH,null=True,blank=True,max_length=30)
    decorations = models.CharField(choices=DEC_CH,null=True,blank=True,max_length=30)
    men_wears = models.CharField(choices=MEN_WEAR_CH,null=True,blank=True,max_length=30)
    women_wears = models.CharField(choices=WOMEN_WEAR_CH,null=True,blank=True,max_length=30)
    kids = models.CharField(choices=KIDS_CH,null=True,blank=True,max_length=30)


class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=15,null=False,blank=False)
    image = models.ImageField(default='product_pics/download.png',null=False,blank=False,upload_to='product_pics')
    video = models.FileField(upload_to ='product_videos', null=True, blank=True)
    CAT_CH=(
        ('electronics','Electronics'),
        ('decorations','Decorations'),
        ('men wears','Men Wears'),
        ('women wears','Women Wears'),
        ('kids','Kids'),
        ('groceries','Groceries'),
        ('cosmetics','Cosmetics'),
        ('books','Books'),
        ('furnitures','Furnitures')
    )
    category = models.CharField(choices=CAT_CH,max_length=20,blank=True)
    subcategory = models.CharField(null=False,blank=False,max_length=30,default='------')

    def __str__(self):
        return "%s is of %s"%(self.name,self.user.username)


