from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.decorators import action

from like.serializers import LikeUserSerializer
from rating.serializers import ReviewSerializer, ReviewActionSerializer
# from rating.serializers import ReviewActionSerializer
from .models import Product
from . import serializers
from .permissions import IsAuthor


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'create'):
            return [permissions.IsAdminUser(), ]
        return [permissions.IsAuthenticatedOrReadOnly(), ]

    # api/v1/products/<id>/reviews/
    # @action(['GET', 'POST'], detail=True)
    # def reviews(self, request, pk):
    #     product = self.get_object()
    #     if request.method == 'GET':
    #         reviews = product.reviews.all()
    #         serializer = ReviewActionSerializer(reviews, many=True).data
    #         return response.Response(serializer, status=200)
    #     else:
    #         if product.reviews.filter(user=request.user).exists():
    #             return response.Response('You already reviewed this product!',
    #                                      status=400)
    #         data = request.data  # rating text
    #         serializer = ReviewActionSerializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(user=request.user, product=product)
    #         return response.Response(serializer.data, status=201)

    # api/v1/product/id/review_delete/
    # @action(['DELETE'], detail=True)
    # def review_delete(self, request, pk):
    #     product = self.get_object()  # Product.objects.get(id=pk)
    #     user = request.user
    #     if not product.reviews.filter(user=user).exists():
    #         return response.Response('You didn\'t reviewed this product!',
    #                                  status=400)
    #     review = product.reviews.get(user=user)
    #     review.delete()
    #     return response.Response('Successfully deleted', status=204)

    # @action(['GET'], detail=True)
    # def reviews(self, request, pk):
    #     product = self.get_object()
    #     reviews = product.reviews.all()
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return Response(serializer.data, status=200)

    # @cache_page(60 * 15)
    @action(['GET'], detail=True)
    def likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        total_likes = likes.count()  # Получить общее количество лайков
        response_data = {
            'likes': serializer.data,
            'total_likes': total_likes
        }
        return Response(response_data, status=200)
