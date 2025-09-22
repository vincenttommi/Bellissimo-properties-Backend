
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class  IsLanlord(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == 'landlord'

class  IsTenant(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == 'tenant'

class IsAdminOrLandlord(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in ['admin','landlord']
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def  has_object_permission(self,request,view, obj):
        if request.user.role == 'admin':
            return True
        if hasattr(obj, 'landlord') and  obj.landlord == request.user:
            return True
        if hasattr(obj,'tenant') and obj.tenant == request.user:
            return True
        return False