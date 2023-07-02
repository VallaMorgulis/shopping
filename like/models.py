from django.contrib.auth import get_user_model
from django.db import models

from account.models import CustomUser
from product.models import Product

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='likes',
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'product']
