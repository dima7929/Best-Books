from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('books/', BookPage.as_view(), name='books'),
    path('news/', NewsPage.as_view(), name='news'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('authors/', AuthorsPage.as_view(), name='authors'),
    path('authors/<slug:author_slug>', ShowAuthor.as_view(), name='show_author'),
    path('book/<slug:book_slug>', ShowBook.as_view(), name='show_book'),
    path('book/caregories/<slug:category_slug>', BookCategories.as_view(), name='show_books_category'),
    path('book/authors/<slug:author_slug>', BookAuthor.as_view(), name='show_books_author'),
    path('book/countries/<slug:country_slug>', BookCountry.as_view(), name='show_books_country'),
    path('authors/countries/<slug:country_slug>', AuthorsCountry.as_view(), name='show_authors_country'),
    path('book/add_book/', AddBook.as_view(), name='add_book'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout')
]


