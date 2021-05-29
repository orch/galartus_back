from rest_framework.permissions import IsAuthenticated, BasePermission


class StaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and \
               (request.user.is_admin or request.user.is_employee)


class StaffOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and \
               request.user.is_employee


class UserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_user


class StaffOrAdminOrUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and \
               (request.user.is_admin or request.user.is_employee or request.user.is_user)
