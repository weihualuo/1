# -*- coding: utf-8 -*-

from rest_framework import permissions

IsAuthenticatedOrReadOnly = permissions.IsAuthenticatedOrReadOnly

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        owner = getattr(obj, 'author', None) or getattr(obj, 'user', None) or getattr(obj, 'starter', None)
        return (owner==request.user)


class IsParentOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS):
            return True
        return (view.parent.author==request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (view.parent.author==request.user)
