from rest_framework import permissions

class IsCustomAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_admin", False))
