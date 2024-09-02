from rest_framework.permissions import BasePermission


class IsSoloAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='solo_admin').exists()