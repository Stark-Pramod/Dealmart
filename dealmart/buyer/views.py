from buyer.serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from buyer.permissions import IsOwnerOrReadOnly,IsUser
from django.http import JsonResponse
# from rest_framework.authtoken import JWTtoken


# Create your views here.
class SignUp(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(username=request.POST.get('username'),
                                        email=request.POST.get('email'),
                                        password=request.POST.get('password'),
                                        first_name = request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name')
                                        )
        user.save()
        return Response({'details': 'user is created'}, status=status.HTTP_201_CREATED)



