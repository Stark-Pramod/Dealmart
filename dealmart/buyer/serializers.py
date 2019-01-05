from rest_framework import serializers

from .models import *
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import exceptions
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
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
    pass_cnf = serializers.CharField(style={'input_type':'password'},required=True)

    class Meta:
        model = User
        fields = ('id','username', 'email','password','pass_cnf')


    def validate(self, data):

        password = data.get('password')
        pass_cnf = data.get('pass_cnf')

        if password != pass_cnf:
               raise exceptions.ValidationError("Password didn't matched ")
        else:
            return data

class OTPSerializer(serializers.ModelSerializer):


    class Meta:
        model = OTP
        fields = ['otp']

class LoginSerializer(serializers.ModelSerializer):

    uname_or_em = serializers.CharField(allow_null=False,required=True)
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)

    class Meta:
        model = User
        fields = ('uname_or_em','password')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        phone_number = data.get('phone_number')
        if not phone_number:
            raise exceptions.ValidationError("Phone number is required!")
        else:
            return data
    #
    # def create(self, validated_data):
    #     pass





