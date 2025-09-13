from rest_framework.permissions import BasePermission

class IsMember(BasePermission):
    message = "Members only."

    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.groups.filter(name="members").exists())
