from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.title')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'product',
                  'product_name', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
