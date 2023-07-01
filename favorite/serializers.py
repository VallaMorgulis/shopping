from rest_framework import serializers
from .models import Favorite


class FavoriteUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        repr = super(FavoriteUserSerializer, self).to_representation(instance)
        repr['product_title'] = instance.product.title
        preview = instance.product.image
        repr['product_preview'] = preview.url if preview else None
        return repr


class FavoriteSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    product_name = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Favorite
        exclude = ('user', )

    def to_representation(self, instance):
        repr = super(FavoriteSerializer, self).to_representation(instance)
        # repr['product_title'] = instance.product.title
        preview = instance.product.image
        repr['product_preview'] = preview.url if preview else None
        return repr

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']
        if user.favorites.filter(product=product).exists():
            raise serializers.ValidationError(
                'You already favorited this product'
            )
        return attrs
