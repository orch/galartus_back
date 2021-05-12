from rest_framework.permissions import IsAuthenticated, BasePermission


class StaffAndAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (not request.user.is_user or request.user.is_admin) and \
               request.user.is_active and request.user.is_employee


class UserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_user
