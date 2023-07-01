# from django.db import models
#
# from account.models import CustomUser
# from product.models import Product
#
#
# class Like(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='likes',
#                              on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='likes',
#                                 on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ['user', 'product']
