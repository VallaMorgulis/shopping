from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from order.serializers import OrderSerializer


class CreateOrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        # orders = user.orders.filter(user=user).order_by('-id')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)

