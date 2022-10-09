from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from main.models import Comment


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CommentForm(ModelForm):
    text_of_comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('text_of_comment',)
