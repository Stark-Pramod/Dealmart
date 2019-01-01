from .serializers import UserSerializer,OTPSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from dealmart.settings import EMAIL_HOST_USER
from random import *
from rest_framework import permissions
from .models import OTP
from django.contrib.auth import login, authenticate,logout


# Create your views here.
class SignUp(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(username = username):
            return Response({'detail':'Username already taken'},status=status.HTTP_306_RESERVED)
        if User.objects.filter(email= email):
            return Response({'detail':'Email already in use'},status=status.HTTP_306_RESERVED)
        if serializer.is_valid():
            user= User.objects.create_user(username=request.data.get('username'),
                                                        email=request.data.get('email'),
                                                        password=request.data.get('password'),
                                                        first_name = request.data.get('first_name'),
                                                        last_name=request.data.get('last_name'),)
            otp = randint(100000, 1000000)
            data = OTP.objects.create(otp=otp,receiver= user)
            code = OTPSerializer(data=data)
            if code.is_valid():
                code.save()
            user.is_active = False
            user.save()
            subject = 'Activate Your Dealmart Account'
            message = render_to_string('account_activate.html', {
                'user': user,
                'OTP': otp,
            })
            from_mail = EMAIL_HOST_USER
            to_mail = [user.email]
            send_mail(subject, message, from_mail, to_mail, fail_silently=False)
            return Response({'details': username+',Please confirm your email to complete registration.'},
                            status=status.HTTP_201_CREATED)
        return Response({'details':'Data not Valid'},status = status.HTTP_406_NOT_ACCEPTABLE)

class Activate(APIView):

    def post(self,request, *args, **kwargs):
        code = request.data.get('otp')
        try:
            user = User.objects.get(pk=request.user.id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and user.otp == code:
            user.is_active = True
            user.save()
            login(request, user)
            return Response({'message': 'Thank you for Email Verfication you are successfully logged in',},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message':'authentication error,Try again',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
