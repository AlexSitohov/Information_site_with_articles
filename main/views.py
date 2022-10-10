from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.forms import *
from main.models import *


def main_view(request):
    if request.method == 'GET' and request.GET.get('search'):
        data = request.GET
        articles = Article.objects.filter(status=True, title__icontains=data.get('search')).order_by('-date')
        context = {'articles': articles}
        return render(request, 'main/main.html', context)
    else:
        articles = Article.objects.filter(status=True, ).order_by('-date')
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
        return HttpResponse('Статья еще не прошла проверку...')


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


def new_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            article.author = request.user
            article.save()

            # article = Article.objects.create(title=form.cleaned_data['title'],
            #                                  text=form.cleaned_data['text'],
            #                                  image=form.cleaned_data['image'],
            #                                  author=request.user,
            #                                  status=False)
            #
            # article.save()
            # for tag in newtags:
            #     tag, created = Tag.objects.get_or_create(name_of_tag=tag)
            #     article.tag.add(tag)

            return redirect('main')
    else:
        form = ArticleForm()
        context = {'form': form}
        return render(request, 'main/new_article.html', context)


def my_articles_view(request):
    articles = Article.objects.filter(author=request.user).order_by('-date')
    context = {'articles': articles}
    return render(request, 'main/my_articles.html', context)
