from rest_framework.permissions import BasePermission


class IsSoloAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='solo_admin').exists()
    
class IsAdminEmpresa(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='resp_empresa').exists()