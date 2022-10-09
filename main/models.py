from django.contrib.auth.models import User
from django.db import models
from django.db.models import *


class Article(Model):
    title = CharField(max_length=50, verbose_name='Заголовок')
    text = TextField(verbose_name='Текст статьи')
    author = ForeignKey(User, on_delete=CASCADE, verbose_name='Автор')
    image = ImageField(verbose_name='Картинка')
    status = BooleanField(default=False, verbose_name='Статус статьи')
    tag = ManyToManyField('Tag', verbose_name='Теги', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'


class Tag(Model):
    name_of_tag = CharField(max_length=100, verbose_name='тэг')

    def __str__(self):
        return self.name_of_tag

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Comment(Model):
    text_of_comment = CharField(max_length=100, verbose_name='Комментарий')
    article = ForeignKey(Article, on_delete=CASCADE, verbose_name='Статья')
    comment_author = ForeignKey(User, on_delete=CASCADE, verbose_name='Автор комментария')
    date = DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')

    def __str__(self):
        return self.text_of_comment

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
