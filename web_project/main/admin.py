from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.



"Настройка админ панели"


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'time_upload', 'get_html_photo')     # Отображение в админ панели
    search_fields = ('title', 'content')        # Поиск по словам
    ordering = ('time_upload', )                # Сортировка по времени создания
    date_hierarchy = 'time_upload'              # Навигация по датам
    prepopulated_fields = {'slug': ("title",)}

    readonly_fields = ('time_upload', 'get_html_photo')
    fields = ('title', 'author', 'slug', 'content', 'year_of_creation', 'price',
              'get_html_photo', 'category', 'country', 'time_upload')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src = '{object.photo.url}' width=60")

    get_html_photo.short_description = 'Фото'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'get_html_photo')
    prepopulated_fields = {'slug': ("name",)}
    search_fields = ('name',)
    ordering = ('name',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src = '{object.photo.url}' width=60")

    get_html_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}
    search_fields = ('name',)
    ordering = ('name',)


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Book, BooksAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)

'Переопределение заголовка админ панели'
admin.site.site_title = 'Администрирование'
admin.site.site_header = 'Администрирование'