from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken import JWTtoken


# Create your views here.
class SignUp(generics.CreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(request.POST)
        if user.is_valid():
            user.save()
            token = JWTtoken.objects.create(user=user)
            return Response({'details':'user is created with token :'+token.key}, status=status.HTTP_201_CREATED)
        return Response("oops sorry", status=status.HTTP_400_BAD_REQUEST)



