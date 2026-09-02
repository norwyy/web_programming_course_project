from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Max, Min
from django.contrib.auth.models import User
from .models import Author, Genre, Series, Publisher, Book
from .serializers import *


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ('list', 'retrieve', 'get_stats'):
            if self.request.user.is_authenticated and self.request.user.is_superuser and self.request.query_params.get('user'):
                user_id = self.request.query_params.get('user')
                qs = qs.filter(user_id=user_id)
            return qs
        else:
            if self.request.user.is_authenticated:
                if not self.request.user.is_superuser:
                    qs = qs.filter(user=self.request.user)
                elif self.request.query_params.get('user'):
                    user_id = self.request.query_params.get('user')
                    qs = qs.filter(user_id=user_id)
            else:
                qs = qs.none()
        return qs

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(count=Count('*'))
        
        top_author = qs.annotate(book_count=Count('books')).order_by('-book_count').first()
        if top_author:
            stats['top_author_name'] = top_author.full_name
            stats['top_author_books_count'] = top_author.book_count
        else:
            stats['top_author_name'] = None
            stats['top_author_books_count'] = None
        
        serializer = AuthorStatsSerializer(instance=stats)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ('list', 'retrieve', 'get_stats'):
            if self.request.user.is_authenticated and self.request.user.is_superuser and self.request.query_params.get('user'):
                user_id = self.request.query_params.get('user')
                qs = qs.filter(user_id=user_id)
            return qs
        else:
            if self.request.user.is_authenticated:
                if not self.request.user.is_superuser:
                    qs = qs.filter(user=self.request.user)
                elif self.request.query_params.get('user'):
                    user_id = self.request.query_params.get('user')
                    qs = qs.filter(user_id=user_id)
            else:
                qs = qs.none()
        return qs

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(count=Count('*'))
        
        top_genre = qs.annotate(book_count=Count('books')).order_by('-book_count').first()
        if top_genre:
            stats['top_genre_name'] = top_genre.name
            stats['top_genre_books_count'] = top_genre.book_count
        else:
            stats['top_genre_name'] = None
            stats['top_genre_books_count'] = None
        
        serializer = GenreStatsSerializer(instance=stats)
        return Response(serializer.data)


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ('list', 'retrieve', 'get_stats'):
            if self.request.user.is_authenticated and self.request.user.is_superuser and self.request.query_params.get('user'):
                user_id = self.request.query_params.get('user')
                qs = qs.filter(user_id=user_id)
            return qs
        else:
            if self.request.user.is_authenticated:
                if not self.request.user.is_superuser:
                    qs = qs.filter(user=self.request.user)
                elif self.request.query_params.get('user'):
                    user_id = self.request.query_params.get('user')
                    qs = qs.filter(user_id=user_id)
            else:
                qs = qs.none()
        return qs

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(count=Count('*'))
        serializer = SeriesStatsSerializer(instance=stats)
        return Response(serializer.data)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ('list', 'retrieve', 'get_stats'):
            if self.request.user.is_authenticated and self.request.user.is_superuser and self.request.query_params.get('user'):
                user_id = self.request.query_params.get('user')
                qs = qs.filter(user_id=user_id)
            return qs
        else:
            if self.request.user.is_authenticated:
                if not self.request.user.is_superuser:
                    qs = qs.filter(user=self.request.user)
                elif self.request.query_params.get('user'):
                    user_id = self.request.query_params.get('user')
                    qs = qs.filter(user_id=user_id)
            else:
                qs = qs.none()
        return qs

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(count=Count('*'))
        serializer = PublisherStatsSerializer(instance=stats)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'genre', 'series', 'publisher').all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BookWriteSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ('list', 'retrieve', 'get_stats'):
            if self.request.user.is_authenticated and self.request.user.is_superuser and self.request.query_params.get('user'):
                user_id = self.request.query_params.get('user')
                qs = qs.filter(user_id=user_id)
            return qs
        else:
            if self.request.user.is_authenticated:
                if not self.request.user.is_superuser:
                    qs = qs.filter(user=self.request.user)
                elif self.request.query_params.get('user'):
                    user_id = self.request.query_params.get('user')
                    qs = qs.filter(user_id=user_id)
            else:
                qs = qs.none()
        return qs

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(
            count=Count('*'),
            avg_year=Avg('year'),
            max_year=Max('year'),
            min_year=Min('year')
        )
        serializer = BookStatsSerializer(instance=stats)
        return Response(serializer.data)