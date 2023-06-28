from django.db import models

from account.models import CustomUser
from product.models import Product


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, related_name='favorites',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favorites',
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'product']
