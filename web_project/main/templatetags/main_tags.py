from django import template
from main.models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_books():
    return Book.objects.all()

@register.simple_tag()
def get_authors():
    return Author.objects.all()
