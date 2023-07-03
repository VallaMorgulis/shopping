from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


# class IsAuthorOrAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
#                 return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj.user or request.user.is_staff
