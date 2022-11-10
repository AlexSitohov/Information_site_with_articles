from django.contrib import messages, auth
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from main.forms import *
from main.models import *


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


class AuthorFilterMain(ListView):
    model = Article
    template_name = 'main/main.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author__username=self.kwargs['username'])


def article_view(request, pk):
    article = Article.objects.select_related('author').prefetch_related('tag').get(id=pk)
    comments = Comment.objects.select_related('comment_author').filter(article=article)
    author = CustomUser.objects.get(username=article.author.username)
    liked = False
    in_favorite = False
    sub = False
    if article.likes.filter(id=request.user.id).exists():
        liked = True
    if article.in_favorite.filter(id=request.user.id).exists():
        in_favorite = True
    if author.subscribers.filter(id=request.user.id).exists():
        sub = True

    if article.status:

        if request.method == 'POST' and request.POST.get('text_of_comment'):
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
            articles_from_same_author = Article.objects.select_related('author').prefetch_related('tag').filter(
                author=article.author).exclude(id=pk).order_by("?")[0:4]
            context = {'article': article, 'comments': comments, 'form': form,
                       'articles_from_same_author': articles_from_same_author,
                       'liked': liked,
                       'in_favorite': in_favorite,
                       'sub': sub}
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
                messages.success(request, 'вы успешно зарегистрировались')
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
                messages.success(request, 'вы успешно вошли')

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
        newtags = request.POST.get('newtags').replace(' ', '').split(',')
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
            if newtags != ' ':
                for tag in newtags[:5]:
                    tag, created = Tag.objects.get_or_create(name_of_tag=tag)
                    article.tag.add(tag)
                messages.success(request, 'ваша статья отправлена на проверку')

                return redirect('main')
    else:
        form = ArticleForm()
        context = {'form': form}
        return render(request, 'main/new_article.html', context)


def my_articles_view(request):
    articles_list = Article.objects.select_related('author').prefetch_related('tag').filter(
        author=request.user).order_by('-status', '-date')
    paginator = Paginator(articles_list, 10)

    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    context = {'articles': articles}
    return render(request, 'main/my_articles.html', context)


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


def delete_article_check_view(request, pk):
    article = Article.objects.get(id=pk)
    if article.author == request.user:
        context = {'article': article}
        messages.error(request, f'Вы точно хотите удалить {article}?')

        return render(request, 'main/delete_article_check.html', context)


def delete_article_view(request, pk):
    article = Article.objects.get(id=pk)
    if article.author == request.user:
        article.delete()
        messages.error(request, 'Статья успешно удалена')

        return redirect('main')


def author_view(request, slug_name):
    author = CustomUser.objects.get(username=slug_name)
    sub = False
    if author.subscribers.filter(id=request.user.id).exists():
        sub = True
    articles_list = Article.objects.select_related('author').prefetch_related('tag').filter(status=True,
                                                                                            author__username=slug_name).order_by(
        '-date')
    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    context = {'articles': articles, 'author': author, 'sub': sub}
    return render(request, 'main/author.html', context)


def like_article_view(request, pk):
    article = Article.objects.get(id=pk)
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article', args=[str(pk)]))


def add_to_fav_article_view(request, pk):
    article = Article.objects.get(id=pk)
    in_favorite = False
    if article.in_favorite.filter(id=request.user.id).exists():
        article.in_favorite.remove(request.user)
        in_favorite = False
    else:
        article.in_favorite.add(request.user)
        in_favorite = True
    return HttpResponseRedirect(reverse('article', args=[str(pk)]))


def favorites_view(request):
    articles_list = Article.objects.filter(in_favorite=request.user).select_related('author').prefetch_related('tag')
    paginator = Paginator(articles_list, 10)
    search_articles = request.GET.get('search')
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    context = {
        'articles': articles
    }
    return render(request, 'main/favorites.html', context)


def my_profile_view(request):
    user = CustomUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.avatar = form.cleaned_data.get('avatar')
            user.save()
        return redirect('my_profile')

    else:
        form = UserEditForm(initial={
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar}
        )
    context = {
        'my_profile': user,
        'user': user,
        'form': form
    }
    return render(request, 'main/my_profile.html', context)


def my_profile_edit_view(request, pk):
    user = CustomUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.avatar = form.cleaned_data.get('avatar')
            user.save()
        return redirect('my_profile')

    else:
        form = UserEditForm(initial={
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar}
        )
        context = {
            'user': user,
            'form': form
        }
        return render(request, 'main/my_profile_edit.html', context)


def subscribe_view(request, slug_name):
    user = request.user
    author = CustomUser.objects.get(username=slug_name)
    sub = False
    if author.subscribers.filter(id=request.user.id).exists():
        author.subscribers.remove(request.user)
        user.subscriptions.remove(author)
        messages.success(request, f'вы отписались от {author}')

        sub = False
    else:
        author.subscribers.add(request.user)
        user.subscriptions.add(author)
        messages.success(request, f'теперь вы подписаны на {author}')

        sub = True

    return HttpResponseRedirect(reverse('author', args=[str(slug_name)]))


def my_subscriptions_view(request):
    my_subscriptions_authors = CustomUser.objects.filter(subscribers=request.user)
    context = {'my_subscriptions_authors': my_subscriptions_authors}
    return render(request, 'main/my_subscriptions.html', context)


def my_subscribers_view(request):
    my_subscribers = CustomUser.objects.filter(subscriptions=request.user)
    context = {'my_subscribers': my_subscribers}
    return render(request, 'main/my_subscribers.html', context)


class FilterTagView(ListView):
    template_name = 'main/main.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = Article.objects.filter(tag__name_of_tag__in=self.request.GET.getlist('tag'),status=True)
        return set(queryset)
