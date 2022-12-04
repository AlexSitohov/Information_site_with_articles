from rest_framework import serializers

from main.models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'image', 'date', 'status', 'tag', 'author', 'likes', 'in_favorite']
        read_only_fields = ('likes', 'in_favorite', 'status')


class CustomUsersSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())

    class Meta:
        model = CustomUser
        fields = ('username', 'articles')
