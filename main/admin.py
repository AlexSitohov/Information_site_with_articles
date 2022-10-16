from django.contrib.admin import register, ModelAdmin

from main.models import *


@register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author', 'image', 'date', 'status',)
    list_display_links = ('title',)
    list_editable = ('status',)


@register(Tag)
class TagAdmin(ModelAdmin):
    pass


@register(Comment)
class CommentAdmin(ModelAdmin):
    pass
