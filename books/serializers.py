from rest_framework import serializers
from .models import Author, Genre, Series, Publisher, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'biography', 'picture']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'name', 'description']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'year', 'description', 'picture',
            'author', 'genre', 'series', 'publisher'
        ]


class BookWriteSerializer(serializers.ModelSerializer):
    """Для создания и обновления книги — только ID связей."""
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'year', 'description', 'picture',
            'author', 'genre', 'series', 'publisher'
        ]
