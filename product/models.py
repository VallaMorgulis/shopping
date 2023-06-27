from random import randint

from django.db import models

from account.models import CustomUser
from category.models import Category


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='products', null=True)
    preview = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category} - {self.title[:25]}'

    class Meta:
        ordering = ('created_at',)


class ProductImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    def generate_name(self):
        return 'image' + str(randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(ProductImage, self).save(*args, **kwargs)
