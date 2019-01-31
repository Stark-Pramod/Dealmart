from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
import json
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for creating user object
    """
    email = serializers.EmailField(required=True,allow_blank=False,allow_null=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="email already exists!",
                                                               lookup='exact')])
    username = serializers.CharField(required=True,allow_blank=False,allow_null=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="username is taken!,try another",
                                                                 lookup='exact')])
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)
    confirm_password = serializers.CharField(style={'input_type':'password'},required=True)

    class Meta:
        model = User
        fields = ('id','username', 'email','password','confirm_password')

    def validate(self, data):

        """
        function for password validation
        :param data:
        :return:
        """
        password = data.get('password')
        pass_cnf = data.get('confirm_password')

        if password != pass_cnf:
               raise ValidationError("Password didn't matched ")
        if len(password) < 6:
               raise ValidationError("password of minimum 6 digit is required")
        else:
            return data


class OTPSerializer(serializers.ModelSerializer):
    """
    serializer for otp
    """

    class Meta:
        model = OTP
        fields = ['otp']

class LoginSerializer(serializers.ModelSerializer):
    """
    login serializer
    """

    uname_or_em = serializers.CharField(allow_null=False,required=True)
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)

    class Meta:
        model = User
        fields = ('uname_or_em','password')


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id',)



class DeliveryAddressSerializer(serializers.ModelSerializer):
    """
    serializer for delivery address
    """

    class Meta:
        model = DeliveryAddress
        fields = '__all__'
        read_only_fields = ('user',)


class PickupAddressSerializer(serializers.ModelSerializer):
    """
    serializer for pickup address
     """
    class Meta:
        model = PickupAddress
        fields = '__all__'
        read_only_fields = ('user',)


class SellerDetailsSerializer(serializers.ModelSerializer):

    """
    serializer for seller detail
    """

    class Meta:
        model = SellerDetails
        fields = '__all__'
        read_only_fields= ('user',)

    # def validate(self, data):
    #     """
    #    -----validating bank account number--------
    #    """
    #     acc_no = data.get('bank_account_no')
    #     if len(str(acc_no)) <9 or len(str(acc_no))>18:
    #          raise ValidationError("Invalid Account number.Account number must be of 9 to 18 digits")
    #
    #     #-----------validating IFSC Code-----------
    #     ifsc = data.get('IFSC_code')
    #     if len(ifsc) != 11:
    #         raise ValidationError("IFSC code should be of 11 character.")
    #     if not ifsc.isalnum():
    #         raise ValidationError("IFSC code is Invalid.")
    #
    #     #-----------validating Aadhar Number -------
    #     aadhar = data.get('aadhar_no')
    #     if len(str(aadhar))!= 12:
    #         raise ValidationError("Aadhar number should be of 12 digits.")
    #
    #     #-----------Validating PAN number----------
    #     pan = data.get('pan_card_no')
    #     if len(pan) != 10:
    #         raise ValidationError("PAN number should be 10 character long.")
    #     if not pan.isalnum():
    #         raise ValidationError("PAN Number is Invalid.")
    #
    #
    #     else:
    #         return data

#
# def get_my_choices(category):
#
#     if category == "electronics":
#         choice_list = (
#             ('mobile','Mobile'),
#             ('Laptop','Laptop'),
#             ('earphone','Earphone'),
#             ('speaker','Speaker'),
#             ('air_conditioner','Air Conditioner'),
#             ('washing_machine','Washing Machine'),
#             ('water_pump','Water Pump'),
#             ('hair_drier','Hair Drier'),
#             ('projector','Projector'),
#             ('desktop','Desktop'),
#             ('cpu','CPU'),
#             ('mouse','Mouse'),
#             ('keyboard','Keyboard'),
#             ('other','Other')
#         )
#     elif category == 'men':
#         choice_list = (
#                 ('shirt','Shirt'),
#                 ('t-shirt','T-shirt'),
#                 ('jeans','Jeans'),
#                 ('pant','Pant'),
#                 ('trouser','Trouser'),
#                 ('jacket','Jacket'),
#                 ('suit','Suit')
#             )
#     elif category == 'women':
#         choice_list = (
#             ('top','Top'),
#             ('jeans','Jeans'),
#             ('saari','Saari'),
#             ('lehnga','Lehnga'),
#             ('t-shirt','T-shirt'),
#             ('suit','Suit'),
#             ('salwar','Salwar'),
#         )
#     elif category == 'kids':
#         choice_list = (
#                 ('cap','Cap'),
#                 ('shirt','Shirt'),
#                 ('inner_wear','Inner Wear'),
#                 ('diaper','Diaper'),
#                 ('t-shirt','T-shirt'),
#                 ('half-pant','Half Pant'),
#                 ('full-pant','Full Pant'),
#                 ('bottle','Bottle')
#             )
#     elif category == 'decoration':
#         choice_list= (
#             ('vase','Vase'),
#             ('painting','Painting'),
#             ('statue','Statue'),
#             ('curtain','Curtain'),
#             ('bedsheet','Bedsheet'),
#         )
#     else:
#         choice_list = (
#             ('others','others')
#         )
#     return choice_list


def get_choices(category):
    # category = self.kwargs['category']
        # category_choice = Category.objects.get(category=category)
        subcats = Subcategory.objects.filter(category=category)
        choice = [(subcat.subcategory,subcat.subcategory.capitalize()) for subcat in subcats]
        return choice


class ListSubcategorySerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(ListSubcategorySerializer, self).__init__(*args,**kwargs)
        if self.context:
            category = self.context['category']
            try:
                category_choice = Category.objects.get(category=category)
            except Category.DoesNotExist:
                category_choice = None
            if category_choice is not None:
                self.fields['subcategory'] = serializers.ChoiceField(
                                             choices=get_choices(category=category_choice))


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='Brand/Label')
    # subcategory_chosen = ListSubcategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('user','subcategory')

    def create(self, validated_data):
        # subcategory_data = validated_data.pop('subcategory')
        # print(subcategory_data)
        product = Product.objects.create(**validated_data)
        return product

    def validate(self, data):
        video = data.get('video')
        image = data.get('image')
        limit_v = 50 * 1024 * 1024
        limit_i = 3 * 1024 * 1024
        if video and video.size > limit_v:
            raise ValidationError('Video too large. Size should not exceed 10 MiB.')
        elif image and image.size > limit_i:
            raise ValidationError('Image too large.Size should not exceed 50 MB')
        else:
            return data


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_field = ('user',)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user',)