from rest_framework import serializers
from .models import Like


class LikeUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Like
        exclude = ('product',)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    product_name = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']
        if user.likes.filter(product=product).exists():
            raise serializers.ValidationError(
                'You already liked this product'
            )
        return attrs


# class FavoriteUserSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.id')
#     user_name = serializers.ReadOnlyField(source='user.get_full_name')
#
#     class Meta:
#         model = Favorite
#         exclude = ('product',)
#
#
# class FavoriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = '__all__'
#
#     def validate(self, attrs):
#         user = self.context['request'].user
#         product = attrs['product']
#         if user.favorites.filter(product=product).exists():
#             raise serializers.ValidationError(
#                 'You already favored this product'
#             )
#         return attrs
#
#     def to_representation(self, instance):
#         repr = super(FavoriteSerializer, self).to_representation(instance)
#         repr['product_title'] = instance.product.title
#         preview = instance.product.preview
#         repr['product_preview'] = preview.url if preview else None
#         return repr
