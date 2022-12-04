from django.shortcuts import render

from rest_framework.viewsets import *

from api.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from api.serializers import *
from main.models import *
from rest_framework.permissions import *


class APIArticleView(ModelViewSet):
    queryset = Article.objects.filter(status=True)
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Article.objects.filter(status=True)
        author = self.request.query_params.get('author')
        min_id = self.request.query_params.get('min_id')
        max_id = self.request.query_params.get('max_id')
        if author:
            queryset = queryset.filter(author__username=author)
        if min_id:
            queryset = queryset.filter(id__gte=min_id)
        if max_id:
            queryset = queryset.filter(id__lte=max_id)
        return queryset


class APICustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = [IsUserOrReadOnly]
