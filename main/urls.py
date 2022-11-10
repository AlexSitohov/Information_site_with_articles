from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from main.views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('author/<slug:username>', AuthorFilterMain.as_view(), name='author_filter'),
    path('article/<int:pk>/', article_view, name='article'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('new_article/', new_article_view, name='new_article'),
    path('my_articles/', my_articles_view, name='my_articles'),
    path('edit_article/<int:pk>/', edit_article_view, name='edit_article'),
    path('delete_article_check/<int:pk>/', delete_article_check_view, name='delete_article_check'),
    path('delete_article/<int:pk>/', delete_article_view, name='delete_article'),
    path('author_page/<slug:slug_name>/', author_view, name='author'),
    path('like_article/<int:pk>', like_article_view, name='like_article'),
    path('add_to_fav_article/<int:pk>', add_to_fav_article_view, name='add_to_fav_article'),
    path('favorites/', favorites_view, name='favorites'),
    path('my_profile/', my_profile_view, name='my_profile'),
    path('my_profile/edit/<int:pk>', my_profile_edit_view, name='my_profile_edit'),
    path('my_profile/password/', PasswordChangeView.as_view(
        template_name='main/password_edit.html',
        success_url=reverse_lazy('password_change_done')),
         name='change_password'),

    path('change_password/done/', PasswordChangeDoneView.as_view(
        template_name='main/password_change_done.html'

    ), name='password_change_done'),
    path('subscribe/<slug:slug_name>/', subscribe_view, name='subscribe'),
    path('my_subscriptions/', my_subscriptions_view, name='my_subscriptions'),
    path('my_subscribers/', my_subscribers_view, name='my_subscribers'),
    path('filter_tag/', FilterTagView.as_view(), name='filter_tag')

]
