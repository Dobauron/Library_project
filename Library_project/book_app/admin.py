from django.contrib import admin
from .models import Book


# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_date', 'ISBN_number', 'number_of_pages', 'URL_to_book_cover',
                    'book_language']
