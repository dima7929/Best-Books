from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Новости', 'url_name': 'news'},
        {'title': 'Книги', 'url_name': 'books'},
        {'title': 'Авторы', 'url_name': 'authors'},
        {'title': 'Контакты', 'url_name': 'contact'}]


"""
Создадим класс, в котором будем хранить информацию,
которая понадобится во многих классах представления.
Классы представления наследуют этот класс
"""


class DataMixin:
        def get_user_context(self, **kwargs):
                context = kwargs

                user_menu = menu.copy()

                context['menu'] = user_menu
                context['categories'] = Category.objects.annotate(Count('book'))
                context['authors'] = Author.objects.annotate(Count('book'))
                context['countries'] = Country.objects.annotate(Count('book'))
                context['random_news'] = News.objects.order_by('?')[:1]
                context['random_books'] = Book.objects.order_by('?')[:4]
                context['random_authors'] = Author.objects.order_by('?')[:2]

                return context