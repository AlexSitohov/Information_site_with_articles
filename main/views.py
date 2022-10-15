from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from main.forms import *
from main.models import *


@csrf_exempt
def main_view(request):
    if request.method == 'GET' and request.GET.get('search'):
        data = request.GET
        articles_list = Article.objects.filter(status=True, title__icontains=data.get('search')).order_by(
            '-date').select_related('author')
        paginator = Paginator(articles_list, 10)
        search_articles = request.GET.get('search')
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
        context = {'articles': articles, 'search_articles': search_articles}
        return render(request, 'main/main.html', context)
    else:
        articles_list = Article.objects.filter(status=True, ).prefetch_related('tag').order_by('-date').select_related(
            'author')
        paginator = Paginator(articles_list, 10)

        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
        context = {'articles': articles}
        return render(request, 'main/main.html', context)


@csrf_exempt
def article_view(request, pk):
    article = Article.objects.select_related('author').prefetch_related('tag').get(id=pk)
    if article.status:
        comments = Comment.objects.select_related('comment_author').filter(article=article)
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


@csrf_exempt
def registration_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'вы успешно зарегистрировались')
                return redirect('main')
        else:
            form = CreateUserForm()
        context = {'form': form}
    else:
        return HttpResponse('Вы уже вошли')

    return render(request, 'main/registration.html', context)


@csrf_exempt
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'вы успешно вошли')

                return redirect('main')
        else:
            form = UserLoginForm()
        context = {'form': form}
        return render(request, 'main/login.html', context)

    else:
        return HttpResponse('Вы уже вошли')


@csrf_exempt
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('main')


@csrf_exempt
def new_article_view(request):
    if request.method == 'POST':
        newtags = request.POST.get('newtags').split(',')
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            # article = form.save()
            # article.author = request.user
            # article.save()

            article = Article.objects.create(title=form.cleaned_data['title'],
                                             text=form.cleaned_data['text'],
                                             image=form.cleaned_data['image'],
                                             author=request.user,
                                             status=False)

            article.save()
            for tag in newtags[:5]:
                tag, created = Tag.objects.get_or_create(name_of_tag=tag)
                article.tag.add(tag)
            messages.success(request, 'ваша статья отправлена на проверку')

            return redirect('main')
    else:
        form = ArticleForm()
        context = {'form': form}
        return render(request, 'main/new_article.html', context)


@csrf_exempt
def my_articles_view(request):
    articles_list = Article.objects.select_related('author').prefetch_related('tag').filter(
        author=request.user).order_by('-status', '-date')
    paginator = Paginator(articles_list, 10)

    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    context = {'articles': articles}
    return render(request, 'main/my_articles.html', context)


@csrf_exempt
def edit_article_view(request, pk):
    article = Article.objects.get(id=pk)
    if article.author == request.user:
        if request.method == 'POST':
            newtags = request.POST.get('newtags').split(',')
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():

                article.title = form.cleaned_data['title']
                article.text = form.cleaned_data['text']
                article.image = form.cleaned_data['image']
                article.status = False

                article.save()

                if newtags:
                    for tag in article.tag.all():
                        tag.delete()

                if newtags:
                    for tag in newtags[:5]:
                        tag, created = Tag.objects.get_or_create(name_of_tag=tag)
                        article.tag.add(tag)
                    messages.success(request, 'ваша статья обновлена и отправлена на проверку')

                return redirect('main')
        else:
            form = ArticleForm()
            tg = ''
            for t in article.tag.all():
                tg += str(t) + ' '

            context = {'form': form, 'article': article, 'tg': tg}
            return render(request, 'main/edit_article.html', context)


@csrf_exempt
def delete_article_check_view(request, pk):
    article = Article.objects.get(id=pk)
    if article.author == request.user:
        context = {'article': article}
        messages.error(request, f'Вы точно хотите удалить {article}?')

        return render(request, 'main/delete_article_check.html', context)


@csrf_exempt
def delete_article_view(request, pk):
    article = Article.objects.get(id=pk)
    if article.author == request.user:
        article.delete()
        messages.error(request, 'Статья успешно удалена')

        return redirect('main')


@csrf_exempt
def author_view(request, slug_name):
    author = User.objects.get(username=slug_name)
    articles_list = Article.objects.select_related('author').prefetch_related('tag').filter(status=True,
                                                                                            author__username=slug_name).order_by(
        '-date')
    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    messages.success(request, f'вы читаете статьи автора {author}')
    context = {'articles': articles}
    return render(request, 'main/author.html', context)
