from django.contrib.auth.models import User, AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import *


class CustomUser(AbstractUser):
    avatar = ImageField('Аватар', null=True, blank=True,
                        validators=[FileExtensionValidator(allowed_extensions=['jpg'])],
                        )
    subscribers = ManyToManyField('CustomUser', related_name='subscribers_users', verbose_name='Подписчики',
                                  blank=True)
    subscriptions = ManyToManyField('CustomUser', related_name='subscriptions_users', verbose_name='Подписки',
                                    blank=True)


class Article(Model):
    title = CharField(max_length=50, verbose_name='Заголовок')
    text = TextField(verbose_name='Текст статьи')
    author = ForeignKey(CustomUser, on_delete=CASCADE, verbose_name='Автор', null=True, blank=True)
    image = ImageField(verbose_name='Картинка')
    date = DateTimeField(auto_now_add=True, verbose_name='Дата написания статьи')
    status = BooleanField(default=False, verbose_name='Статус статьи')
    tag = ManyToManyField('Tag', verbose_name='Теги', null=True, blank=True)
    likes = ManyToManyField(CustomUser, related_name='likes_posts', verbose_name='Лайки', null=True, blank=True)
    in_favorite = ManyToManyField(CustomUser, related_name='favorite_posts',
                                  verbose_name='Избранные статьи у пользователей', null=True, blank=True)

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
    comment_author = ForeignKey(CustomUser, on_delete=CASCADE, verbose_name='Автор комментария')
    date = DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')

    def __str__(self):
        return self.text_of_comment

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
