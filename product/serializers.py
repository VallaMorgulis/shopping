from django.db.models import Avg
from rest_framework import serializers
from category.models import Category
from rating.serializers import ReviewSerializer
# from rating.serializers import ReviewSerializer
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Product
        fields = ('user', 'user_email', 'title', 'price', 'image', 'stock', 'id')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr


class ProductSerializer(serializers.ModelSerializer):
    # user_email = serializers.ReadOnlyField(source='user.email')
    # user = serializers.ReadOnlyField(source='user.id')
    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_stars(instance):
        stars = {
            '5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
            '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
            '1': instance.reviews.filter(rating=1).count()}
        return stars

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['ratings_count'] = instance.reviews.count()
        repr['stars'] = self.get_stars(instance)
        return repr








