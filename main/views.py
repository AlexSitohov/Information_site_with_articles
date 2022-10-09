from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.forms import *
from main.models import *


def main_view(request):
    if request.method == 'GET' and request.GET.get('search'):
        data = request.GET
        articles = Article.objects.filter(status=True, title__icontains=data.get('search'))
        context = {'articles': articles}
        return render(request, 'main/main.html', context)
    else:
        articles = Article.objects.filter(status=True, )
        context = {'articles': articles}
        return render(request, 'main/main.html', context)


def article_view(request, pk):
    article = Article.objects.get(id=pk)
    if article.status:
        comments = Comment.objects.filter(article=article)
        if request.method == 'POST':
            data = request.POST
            comment = Comment.objects.create(
                text_of_comment=data.get('text_of_comment'),
                article=article,
                comment_author=request.user,
            )
            comment.save()
            return redirect('article', article.pk)
        else:
            form = CommentForm()
            context = {'article': article, 'comments': comments, 'form': form}
        return render(request, 'main/article.html', context)
    else:
        return HttpResponse('Статья недоступна')

def registration_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('main')
        else:
            form = CreateUserForm()
        context = {'form': form}
    else:
        return HttpResponse('Вы уже вошли')

    return render(request, 'main/registration.html', context)


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('main')
        else:
            form = UserLoginForm()
        context = {'form': form}
        return render(request, 'main/login.html', context)

    else:
        return HttpResponse('Вы уже вошли')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('main')
