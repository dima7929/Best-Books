from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *

class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.fields['author'].empty_label = 'Автор не выбран'
        self.fields['country'].empty_label = 'Страна не выбрана'

    class Meta:
        model = Book
        fields = ['title', 'slug', 'content', 'author', 'year_of_creation', 'category', 'price', 'country', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        """
        Наша кастомная валидация
        :return:
        """
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Длина превышает 255 символов')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'from-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=127, widget=forms.TextInput(attrs={'class': 'name_field'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'email_field'}))
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'content_field'}))
    capa = CaptchaField()
