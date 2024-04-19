from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuth(BasePermission):
    """Rights only for admin"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated)