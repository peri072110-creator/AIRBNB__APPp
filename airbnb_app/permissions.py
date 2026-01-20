from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsHost(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "HOST"


class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "GUEST"


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == "ADMIN" or obj.owner == request.user
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
