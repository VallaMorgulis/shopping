from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Comment
from .serializers import CommentSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    pagination_class = StandartResultPagination
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser(), ]
        return [permissions.IsAuthenticatedOrReadOnly(), ]
