from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOnly(BasePermission):
    """Give permission to admin only"""

    def has_permission(self, request, view):
        if request.user.user_type == 'A':
            return True
        return False


class UserTypePermission(BasePermission):
    """Give permission to the users based on type of the user"""

    def has_permission(self, request, view):
        user_type = request.user.user_type
        allowed_user_types = getattr(view, 'allowed_user_types', [])
        return user_type in allowed_user_types or request.method in SAFE_METHODS


class UserUpdatePermission(BasePermission):
    """Give permission to logged in user or admin to update only theirs profile"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class FacultyOnly(BasePermission):
    """Give permission to faculty only"""

    def has_permission(self, request, view):
        if request.user.user_type == 'F':
            return True
        return False
