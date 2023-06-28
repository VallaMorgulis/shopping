from django.core.paginator import Paginator
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from favorite.serializers import FavoriteUserSerializer
from like.serializers import LikeUserSerializer
from .models import Product
from . import serializers
from .serializers import ProductListSerializer


class StandartResultPagination(PageNumberPagination):
    # Пагинация на 2 страницы со списком продуктов
    page_size = 2
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'description')
    filterset_fields = ('category', 'price')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.ProductCreateSerializer
        return serializers.ProductDetailSerializer

    def get_permissions(self):
        # создавать, удалять, обновлять, частично обновлять может только админ
        if self.action in ('update', 'delete', 'create'):
            return [permissions.IsAdminUser(), ]
        return [permissions.AllowAny(), ]

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

