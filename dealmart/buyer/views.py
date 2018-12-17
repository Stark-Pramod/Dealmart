from .serializers import UserSerializer,OTPSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from dealmart.settings import EMAIL_HOST_USER
from random import *
from rest_framework import permissions
from .models import OTP


# Create your views here.
class SignUp(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user= User.objects.create_user(username=request.POST.get('username'),
                                        email=request.POST.get('email'),
                                        password=request.POST.get('password'),
                                        first_name = request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),)
        otp = randint(1002, 9999)
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
        messages.success(request, 'Please!Confirm your email to complete registration.')
        return Response({'details': 'user is created'}, status=status.HTTP_201_CREATED)
        # return Response({'details':'error'},status = status.HTTP_406_NOT_ACCEPTABLE)

class Activate(generics.CreateAPIView):

    def post(self,request,user_id, *args, **kwargs):
        code = request.POST.get('otp')
        try:
            user = User.objects.get(pk=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and user.otp == code:
            user.is_active = True
            user.save()
            login(request, user)
            # messages.success(request, 'thank you! for email verification')
            return redirect('edit_profile',user.id)
        else:
            return HttpResponse("invalid link")
