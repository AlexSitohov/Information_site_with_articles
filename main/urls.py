from django.urls import path

from main.views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('article/<int:pk>/', article_view, name='article'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
