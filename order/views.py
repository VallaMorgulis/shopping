# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import viewsets, permissions
# from .models import Order
# from .serializers import OrderSerializer
#
#
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     filter_backends = (DjangoFilterBackend,)  # история заказов
#     filterset_fields = ('user',)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_permissions(self):
#         if self.action in ('update', 'partial_update', 'destroy'):
#             return [permissions.IsAdminUser(), ]
#         return [permissions.IsAuthenticatedOrReadOnly(), ]
