from django.shortcuts import render
from buyer.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status


# Create your views here.
class SignUp(viewsets.ModelViewSet):
    """
    List all snippets, or create a new snippet.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, serializer):
        serializer = UserSerializer(data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, serializer):
        return Response(serializer.data)



