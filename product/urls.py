from django.urls import path, include
from django.views.decorators.cache import cache_page

from product import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.ProductListCreateView.as_view()),
    # path('<int:pk>/', views.ProductDetailView.as_view()),
]
