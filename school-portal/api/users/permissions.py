from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.role == "admin"))

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.role == "teacher" or request.user.role == "admin"))

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For Student objects, allow if the request.user is linked as student or admin
        if getattr(request.user, "is_superuser", False) or request.user.role == "admin":
            return True
        # If the student has a linked user
        if hasattr(obj, "user") and obj.user:
            return obj.user == request.user
        return False