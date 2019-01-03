from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,allow_blank=False,allow_null=False,)
                                   # validators=[UniqueValidator(queryset=User.objects.all(),
                                   #                             message="email is Required",
                                   #                             lookup='exact')])
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)
    pass_cnf = serializers.CharField(style={'input_type':'password'},required=True)

    class Meta:
        model = User
        fields = ('id','username', 'email','password','pass_cnf')


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
        fields = ('first_name','last_name','')




