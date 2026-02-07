from rest_framework import viewsets
from .models import Author, Genre, Series, Publisher, Book
from .serializers import (
    AuthorSerializer,
    GenreSerializer,
    SeriesSerializer,
    PublisherSerializer,
    BookSerializer,
    BookWriteSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'genre', 'series', 'publisher').all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BookWriteSerializer
        return BookSerializer
