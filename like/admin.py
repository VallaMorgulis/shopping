from django.contrib import admin

from like.models import Like


@admin.register(Like)
class Like(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')

