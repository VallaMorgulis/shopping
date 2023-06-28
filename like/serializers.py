from rest_framework import serializers
from .models import Like


class LikeUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Like
        exclude = ('product', )


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


# class FavoriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ('id', 'post')
#
#     def to_representation(self, instance):
#         repr = super(FavoriteSerializer, self).to_representation(instance)
#         repr['post_title'] = instance.post.title
#         preview = instance.post.preview
#         repr['post_preview'] = preview.url if preview else None
#         return repr
