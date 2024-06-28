from django.db import models
from django.urls import reverse

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255,verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Содержание')
    time_upload = models.DateTimeField(auto_now_add=True)
    year_of_creation = models.PositiveSmallIntegerField(verbose_name='Год публикации')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    author = models.ForeignKey('Author', on_delete=models.PROTECT, verbose_name='Автор')
    category = models.ManyToManyField('Category', verbose_name='Категория')
    country = models.ForeignKey('Country', on_delete=models.PROTECT, verbose_name='Страна')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-time_upload', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_book', kwargs={'book_slug': self.slug})




class Author(models.Model):
    name = models.CharField(max_length=63, verbose_name='Имя/Фамилия/Псевдоним')
    country = models.ForeignKey('Country', on_delete=models.PROTECT, verbose_name='Страна')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Страна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('show_author', kwargs={'author_slug': self.slug})

    def get_absolute_url_books(self):
        return reverse('show_books_author', kwargs={'author_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=63, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', 'description']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_books_category', kwargs={'category_slug': self.slug})


class Country(models.Model):
    name = models.CharField(max_length=63, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Флаг')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name', 'slug']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_books_country', kwargs={'country_slug': self.slug})


