from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView

from .models import *
from .forms import *
from .utils import DataMixin

# Create your views here.


class HomePage(DataMixin, TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title="Главная")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class BookPage(DataMixin, ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'main/books.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_selected'] = 0
        context['author_selected'] = 0
        context_from_DataMixin = self.get_user_context(title="Книги")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))

    def get_queryset(self):
        return Book.objects.filter().prefetch_related('category').select_related('author')


class BookCategories(DataMixin, ListView):
    model = Book
    template_name = 'main/books.html'
    context_object_name = 'books'
    allow_empty = False # Если список пуст -> 404
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.filter(category__slug=self.kwargs['category_slug']).prefetch_related(
            'category').select_related('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        k = Category.objects.get(slug=self.kwargs['category_slug'])
        context['category_selected'] = self.kwargs['category_slug']
        context['author_selected'] = 0
        context_from_DataMixin = self.get_user_context(title=f'Категория: {k.name}')
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class BookAuthor(DataMixin, ListView):
    model = Book
    template_name = 'main/books.html'
    context_object_name = 'books'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.filter(author__slug=self.kwargs['author_slug']).prefetch_related(
            'category').select_related('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Author.objects.get(slug=self.kwargs['author_slug'])
        context['category_selected'] = 0
        context['author_selected'] = self.kwargs['author_slug']
        context_from_DataMixin = self.get_user_context(title=f"Книги автора: {a.name}")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class BookCountry(DataMixin, ListView):
    model = Book
    template_name = 'main/books.html'
    context_object_name = 'books'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.filter(country__slug=self.kwargs['country_slug']).prefetch_related(
            'category').select_related('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Country.objects.get(slug=self.kwargs['country_slug'])
        context['category_selected'] = 0
        context['author_selected'] = 0
        context['country_selected'] = self.kwargs['country_slug']
        context_from_DataMixin = self.get_user_context(title=f"Книги: {c.name}")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class AuthorsPage(DataMixin, ListView):
    model = Author
    template_name = 'main/authors.html'
    context_object_name = 'authors_list'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title="Авторы")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class AuthorsCountry(DataMixin, ListView):
    model = Author
    template_name = 'main/authors.html'
    context_object_name = 'authors_list'
    allow_empty = False
    paginate_by = 4

    def get_queryset(self):
        return Author.objects.filter(country__slug=self.kwargs['country_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Country.objects.get(slug=self.kwargs['country_slug'])
        context['category_selected'] = 0
        context['author_selected'] = 0
        context['country_selected'] = self.kwargs['country_slug']
        context_from_DataMixin = self.get_user_context(title=f"Авторы: {c.name}")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class ShowBook(DataMixin, DetailView):
    model = Book
    template_name = 'main/show_book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context()
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class ShowAuthor(DataMixin, DetailView):
    model = Author
    template_name = 'main/show_author.html'
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context()
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'main/add_book.html'
    success_url = reverse_lazy('books')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title='Добавить книгу')
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(context_from_DataMixin.items()))

    def form_valid(self, form):
        """
        С помощью этой функции пользователь будет сразу авторизовываться
        после регистрации
        """
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title='Войти')
        return dict(list(context.items()) + list(context_from_DataMixin.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class ContactPage(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title='Контакты')
        return dict(list(context.items()) + list(context_from_DataMixin.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class NewsPage(DataMixin, ListView):
    model = News
    template_name = 'main/news.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_from_DataMixin = self.get_user_context(title="Новости")
        return dict(list(context.items()) + list(context_from_DataMixin.items()))


