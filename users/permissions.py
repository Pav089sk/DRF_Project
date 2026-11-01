from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Разрешение только для пользователей из группы модераторов.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='moderators').exists()

class IsOwner(permissions.BasePermission):
    """
       Разрешение только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
