from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Product
from . import serializers


class StandartResultPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'description')
    filterset_fields = ('category', 'price')

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.ProductCreateSerializer
        return serializers.ProductDetailSerializer

    def get_permissions(self):
        # создавать, удалять, обновлять, частично обновлять может только админ
        if self.action == 'read':
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]

    # @action(['GET'], detail=True)
    # def comments(self, request, pk):
    #     post = self.get_object()
    #     # print(post, '!!!!!!!!!!!!!!!!')
    #     comments = post.comments.all()
    #     serializer = CommentSerializer(instance=comments, many=True)
    #     return Response(serializer.data, status=200)
    #
    # # ...api/v1/posts/<id>/likes
    # @action(['GET'], detail=True)
    # def likes(self, request, pk):
    #     post = self.get_object()
    #     likes = post.likes.all()
    #     serializer = LikeUserSerializer(instance=likes, many=True)
    #     return Response(serializer.data, status=200)
    #
    # @action(['POST', "DELETE"], detail=True)
    # def favorites(self, request, pk):
    #     post = self.get_object()  # Post.objects.get(id=pk)
    #     user = request.user
    #     favorite = user.favorites.filter(post=post)
    #
    #     if request.method == 'POST':
    #         if favorite.exists():
    #             return Response({'msg': 'Already in Favorite'}, status=400)
    #         Favorite.objects.create(owner=user, post=post)
    #         return Response({'msg': 'Added to favorite'}, status=201)
    #
    #     if favorite.exists():
    #         favorite.delete()
    #         return Response({'msg': 'Deleted from favorite'}, status=204)
    #     return Response({'msg': 'Post Not Found in Favorites'}, status=404)