from django.contrib.admin import register, ModelAdmin

from main.models import *


@register(Article)
class ArticleAdmin(ModelAdmin):
    pass


@register(Tag)
class TagAdmin(ModelAdmin):
    pass
