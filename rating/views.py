# from rest_framework import viewsets, permissions
#
# from .models import Review
# from .serializers import ReviewSerializer
#
#
# class RatingViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_permissions(self):
#         if self.action in ('update', 'partial_update', 'destroy'):
#             return [permissions.IsAdminUser(), ]
#         return [permissions.IsAuthenticatedOrReadOnly(), ]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
