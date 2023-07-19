from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    """
    Пользовательский класс разрешений для проверки, является ли пользователь автором объекта.

    Пользователь может выполнять любые действия над объектом, если он является его автором.

    Атрибуты:
    - request (Request): Объект запроса.
    - view (View): Объект представления (view).
    - obj (Any): Объект, к которому проверяется разрешение.

    Возвращает:
    - bool: True, если пользователь является автором объекта, иначе False.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Пользовательский класс разрешений для проверки, является ли пользователь автором объекта
    или имеет статус администратора.

    Пользователь сможет выполнять операции создания, обновления (update), частичного обновления (partial_update)
    и удаления (destroy) над объектом, если он является его автором или имеет статус администратора.

    Атрибуты:
    - request (Request): Объект запроса.
    - view (View): Объект представления (view).

    Возвращает:
    - bool: True, если пользователь является автором объекта или имеет статус администратора, иначе False.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ['create', 'update', 'partial_update', 'destroy']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_staff

# from rest_framework import permissions
# from rest_framework.permissions import SAFE_METHODS
#
#
# class IsAuthor(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj
#
#
# class IsAuthorOrAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if view.action in ['create', 'update', 'partial_update', 'destroy']:
#                 return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj.owner or request.user.is_staff
