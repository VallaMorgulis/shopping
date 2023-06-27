from rest_framework import serializers

from category.models import Category
from .models import Product, ProductImage


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'category_name', 'preview', 'price',
                  'description')

    # def to_representation(self, instance):
    #     repr = super(ProductListSerializer, self).to_representation(instance)
    #     repr['likes_count'] = instance.likes.count()
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         repr['is_liked'] = user.likes.filter(post=instance).exists()
    #         repr['is_favorite'] = user.favorites.filter(post=instance).exists()
    #     return repr


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True,
                                                  queryset=Category.objects.all())
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        product = Product.objects.create(**validated_data)

        for image in images:
            ProductImage.objects.create(image=image, product=product)
        return product


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['comments_count'] = instance.comments.count()
    #     repr['comment'] = CommentSerializer(
    #         instance.comments.all(), many=True).data  # 2 способ
    #     repr['likes_count'] = instance.likes.count()
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         repr['is_liked'] = user.likes.filter(post=instance).exists()
    #         repr['is_favorite'] = user.favorites.filter(post=instance).exists()
    #     return repr

# class ProductListLikesSerializer(serializers.ModelSerializer):
#     owner_username = serializers.ReadOnlyField(source='owner.username')
#     category_name = serializers.ReadOnlyField(source='category.name')
#
#     class Meta:
#         model = Product
#         fields = ('id', 'owner', 'title', 'owner_username', 'category_name',
#                   'category', 'preview')
