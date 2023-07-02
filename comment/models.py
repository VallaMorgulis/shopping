from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product

User = get_user_model()


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments',
                                on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    user = models.ForeignKey(User, related_name='comments',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.product}'
