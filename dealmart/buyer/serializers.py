from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    OTP = serializers.IntegerField(allow_null=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password','OTP')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise serializers.ValidationError('This email address is already in use.')
