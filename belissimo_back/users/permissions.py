from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsAuthenticatedOrReadOnly(BasePermission):
    """
  Allow GET(list and retrieve) ,HEAD and OPTIONS methods for all users,but restrict POST/PUT/DELETE to authenticated users.
"""
    def has_permission(self, request, view):
        #Allow read-only  access for unauthenticated users
        if request.method in SAFE_METHODS:
            return True
        #Allow write access for authenticated users
        return request.user and request.user.is_authenticated
    

    


    