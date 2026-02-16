from django.contrib import admin
from .models import Author, Genre, Series, Publisher, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'biography', 'picture', 'user')
    list_filter = ('user',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'user')
    list_filter = ('user',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'user')
    list_filter = ('user',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'user')
    list_filter = ('user',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'author', 'genre', 'series', 'publisher', 'picture', 'user')
    list_filter = ('user',)
