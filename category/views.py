from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from category import serializers
from category.models import Category


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        # создавать, удалять, обновлять, частично обновлять может только админ
        if self.action in ('update', 'delete', 'create'):
            return [permissions.IsAdminUser(), ]
        return [permissions.IsAuthenticatedOrReadOnly(), ]
