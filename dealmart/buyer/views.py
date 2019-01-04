from .serializers import *
from .backends import EmailOrUsername
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from dealmart.settings import EMAIL_HOST_USER
from random import *
from rest_framework import permissions
from .models import OTP
from django.contrib.auth import login,logout
from django.utils import timezone
from datetime import datetime, timedelta




# Create your views here.
class SignUp(APIView):
    """
    List all snippets, or create a new snippet.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        pass_cnf = request.data.get('pass_cnf')
        #-------validation of each field--------#
        if not username:
            return Response({'error':'username is required'})
        if not email:
            return Response({'error': 'email field is required'})
        if not password or not pass_cnf:
            return Response({'error': 'password is required'})
        if User.objects.filter(username=username):
            return Response({'detail':'Username already taken'},status=status.HTTP_306_RESERVED)
        if User.objects.filter(email=email):
            return Response({'detail':'Email already in use'},status=status.HTTP_306_RESERVED)
        if password != pass_cnf:
            return Response({'warning': "password didn't match"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        #----------- all field valid -----------#

        if serializer.is_valid():
            user = User.objects.create_user(username=username,email=email,password=password)
            otp = randint(100000, 1000000)
            data = OTP.objects.create(otp=otp,receiver=user)
            data.save()
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
            return Response({'details': username+',Please confirm your email to complete registration.',
                             'user_id': user.id },
                            status=status.HTTP_201_CREATED)
        return Response({'details':'Data not Valid'},status=status.HTTP_406_NOT_ACCEPTABLE)


class Activate(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OTPSerializer


    def post(self,request,user_id,*args,**kwargs):
        code = OTPSerializer(data=request.data)
        if code.is_valid(raise_exception=True):
            print(user_id)
            try:
                otp = OTP.objects.get(receiver=user_id)
            except(TypeError, ValueError, OverflowError, otp.DoesNotExist):
                otp = None
            try:
                receiver = User.objects.get(id=user_id)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                receiver = None
            if otp is None or receiver is None:
                return Response({'error':'you are not a valid user'},status=status.HTTP_400_BAD_REQUEST)

            elif timezone.now() - otp.sent_on >= timedelta(days=0,hours=0,minutes=2,seconds=0):
                otp.delete()
                return Response({'detail':'OTP expired!',
                                 'user_id':user_id})

            if otp.otp == int(code):
                receiver.is_active = True
                receiver.save()
                login(request, receiver)
                otp.delete()
                return Response({'message': 'Thank you for Email Verification you are successfully logged in'},
                            status=status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response({'error':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



class ResendOtp(generics.CreateAPIView):
    serializer_class = OTPSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self,request,user_id,*args,**kwargs):
        try:
            user = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response({'error':'Not a valid user!'})
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver= user)
        data.save()
        subject = 'Activate Your Dealmart Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
        })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': user.username +',Please confirm your email to complete registration.',
                         'user_id': user_id },
                        status=status.HTTP_201_CREATED)

class Login(APIView):
    """
    the user can login either with email or username. EmailOrUsername is the function for it.
    """


    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uname_or_em = serializer.validated_data['uname_or_em']
            password = serializer.validated_data['password']
            user = EmailOrUsername(self,uname_or_em = uname_or_em,password=password)

            if user == 2:
                return Response({'error':'Invalid Username or Email!!'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            elif user == 3:
                return Response({'error':'Incorrect Password'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            else:
                if user.is_active:
                   login(request, user)
                   return Response({'detail':'successfully Logged in!','user_id': user.id})
                else:
                   return Response({'error':'Please! varify Your Email First','user_id':user.id},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)


class Logout(APIView):
    """
    logout view.Only authenticated user can access this url(by default)

    """
    def get(self,request,*args,**kwargs):
        logout(request)
        return Response({'message':'successfully logged out'},
                        status=status.HTTP_200_OK)


class AddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def post(self,request,*args,**kwargs):
        address = AddressSerializer(data=request.data)
        if address.is_valid(raise_exception=True):
            address.save(user=request.user)
            return Response({'message':'address saved successfully'},
                              status=status.HTTP_200_OK)
        return Response({'error':'Not a valid address!'},
                         status = status.HTTP_406_NOT_ACCEPTABLE)








