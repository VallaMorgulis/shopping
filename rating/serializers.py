from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['id', 'product', 'rating', 'user', 'user_full_name', 'created_at']

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
