from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuth(BasePermission):
    """Rights only for admin"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated)


class IsAdmin(BasePermission):
    """Rights only for admin"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='admin').exists() )
    

class IsBussines(BasePermission):
    """Rights only for Login"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='bussines').exists() )


class IsUser(BasePermission):
    """Rights only for user"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='user').exists() )
