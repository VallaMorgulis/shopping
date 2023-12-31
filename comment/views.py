from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from config.tasks import send_comment_notification_email
from .models import Comment
from .serializers import CommentSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    pagination_class = StandartResultPagination
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('product', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        send_comment_notification_email.delay(serializer.data['id'])

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser(), ]
        return [permissions.IsAuthenticatedOrReadOnly(), ]
