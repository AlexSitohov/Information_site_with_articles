from django.urls import path

from main.views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('article/<int:pk>/', article_view, name='article'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('new_article/', new_article_view, name='new_article'),
    path('my_articles/', my_articles_view, name='my_articles'),
    path('edit_article/<int:pk>/', edit_article_view, name='edit_article'),
    path('delete_article_check/<int:pk>/', delete_article_check_view, name='delete_article_check'),
    path('delete_article/<int:pk>/', delete_article_view, name='delete_article'),
    path('author/<slug:slug_name>/', author_view, name='author'),

]
