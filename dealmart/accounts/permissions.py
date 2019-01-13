from rest_framework import permissions
from .models import *

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,

        # Write permissions are only allowed to the owner of the address.
        return obj.user.username == request.user.username


class IsBuyer(permissions.BasePermission):

    def has_permission(self, request, view):
        user =request.user
        roles = user.roles.all()
        for role in roles:
            if role.id == 1:
                return True
            else:
                return False

class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):
        user =request.user
        roles = user.roles.all()
        for role in roles:
            if role.id == 2:
                return True
            else:
                return False

class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.is_staff==True:
            return True
        return False