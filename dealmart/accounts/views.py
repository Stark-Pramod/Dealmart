from .serializers import *
from .permissions import *
from .backends import EmailOrUsername
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework import status
from rest_framework import generics,viewsets
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
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.create_user(username=username,email=email,password=password)
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver=user)
        data.save()
        user.is_active = False
        user.save()
        buyer = Role.objects.get(id=1)
        user.roles.add(buyer)
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



class Activate(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OTPSerializer


    def post(self,request,user_id,*args,**kwargs):
        code = OTPSerializer(data=request.data)
        code.is_valid(raise_exception=True)
        code = code.validated_data['otp']
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

        if otp.otp == code:
            receiver.is_active = True
            receiver.save()
            login(request, receiver)
            otp.delete()
            return Response({'message': 'Thank you for Email Verification you are successfully logged in'},
                            status=status.HTTP_200_OK)
        else:
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
        otp = OTP.objects.filter(receiver=user)
        if otp:
            otp.delete()
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
        serializer.is_valid(raise_exception=True)
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


class RoleView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,IsAdmin)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class DeliveryAddressView(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    queryset = DeliveryAddress.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsBuyer)
    lookup_url_kwarg = 'ad_id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        add = DeliveryAddress.objects.filter(user=request.user)
        serializer = DeliveryAddressSerializer(data=add,many=True)
        serializer.is_valid()
        return Response(serializer.data)


class PickupAddressView(viewsets.ModelViewSet):
    serializer_class = PickupAddressSerializer
    queryset = PickupAddress.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsSeller)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        add = PickupAddress.objects.filter(user=request.user)
        serializer = PickupAddressSerializer(data=add,many=True)
        serializer.is_valid()
        return Response(serializer.data)


class SellerDetailsView(viewsets.ModelViewSet):
    serializer_class = SellerDetailsSerializer
    queryset = SellerDetails.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsSeller,IsOwner)

    def perform_create(self, serializer):
        if SellerDetails.objects.filter(user=self.request.user):
            raise ValidationError("you are not allowed to add more than one detail set")
        serializer.save(user=self.request.user)









