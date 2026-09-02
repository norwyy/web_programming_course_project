from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max, Min
from .models import Author, Genre, Series, Publisher, Book
from .serializers import *


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Необходимо указать username и password'},
                status=400
            )
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        
        return Response(
            {'error': 'Неверные учетные данные'},
            status=401
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Вы успешно вышли из системы'})

class BaseOwnedModelViewSet(viewsets.ModelViewSet):
    stats_serializer_class = None
    stats_annotations = {}
    stats_extra_fields = {}

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        if self.action in ('list', 'retrieve', 'get_stats'):
            if user.is_authenticated and user.is_superuser:
                user_id = self.request.query_params.get('user')
                if user_id:
                    qs = qs.filter(user_id=user_id)
            return qs
        
        if user.is_authenticated:
            if not user.is_superuser:
                qs = qs.filter(user=user)
            elif self.request.query_params.get('user'):
                user_id = self.request.query_params.get('user')
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.none()
        
        return qs

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(count=Count('*'), **self.stats_annotations)
        
        for field_name, (display_name, count_field) in self.stats_extra_fields.items():
            top_obj = qs.annotate(
                item_count=Count(count_field)
            ).order_by('-item_count').first()
            
            if top_obj:
                stats[display_name] = getattr(top_obj, field_name)
                stats[f'{display_name}_count'] = top_obj.item_count
            else:
                stats[display_name] = None
                stats[f'{display_name}_count'] = 0
        
        serializer = self.stats_serializer_class(instance=stats)
        return Response(serializer.data)


class AuthorViewSet(BaseOwnedModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    stats_serializer_class = AuthorStatsSerializer
    stats_extra_fields = {
        'full_name': ('top_author_name', 'books'),
    }


class GenreViewSet(BaseOwnedModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    stats_serializer_class = GenreStatsSerializer
    stats_extra_fields = {
        'name': ('top_genre_name', 'books'),
    }


class SeriesViewSet(BaseOwnedModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    stats_serializer_class = SeriesStatsSerializer


class PublisherViewSet(BaseOwnedModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    stats_serializer_class = PublisherStatsSerializer


class BookViewSet(BaseOwnedModelViewSet):
    queryset = Book.objects.select_related(
        'author', 'genre', 'series', 'publisher'
    ).all()
    stats_serializer_class = BookStatsSerializer
    stats_annotations = {
        'avg_year': Avg('year'),
        'max_year': Max('year'),
        'min_year': Min('year'),
    }

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BookWriteSerializer
        return BookSerializer