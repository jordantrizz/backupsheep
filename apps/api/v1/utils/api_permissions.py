from rest_framework.permissions import BasePermission


class MemberPermissions(BasePermission):
    """Minimal compatibility permission used while the rewrite restores finer-grained rules."""

    message = "Authentication is required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)