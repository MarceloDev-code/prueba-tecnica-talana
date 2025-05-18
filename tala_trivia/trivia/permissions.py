from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    """
    Permite acceso solo si el usuario tiene rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', '') == 'admin'
