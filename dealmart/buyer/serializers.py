from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise serializers.ValidationError('This email address is already in use.')

class OTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTP
        fields = ('otp','receiver',)
