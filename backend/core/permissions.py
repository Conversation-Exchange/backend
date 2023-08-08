"""Кастомные разрешения."""

from rest_framework import permissions


class ActiveChatOrReceiverOnly(permissions.BasePermission):
    """
    Разрешение на отправку сообщений для участников активного чата
    или только для получателя.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj.members.filter(id=request.user.id).exists()
            and (
                obj.is_active
                or not obj.members_info.get(member=request.user).is_creator
            )
        )


class IsAdminOrModeratorReadOnly(permissions.BasePermission):
    """
    Разрешение на просмотр Администраторам или Модераторам.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            return (
                user.is_staff or
                user.role == 'moderator' or
                user.role == 'admin'
            )
        return True
