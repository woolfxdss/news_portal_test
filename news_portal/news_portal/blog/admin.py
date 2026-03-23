"""
    Здесь зарегистрированы модели для приложения 'blog'
"""

from django.contrib import admin
from .models import Post, PostCategory, Subscriber


admin.site.register(Post)
admin.site.register(PostCategory)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email']