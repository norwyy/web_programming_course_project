from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    AuthorViewSet,
    GenreViewSet,
    SeriesViewSet,
    PublisherViewSet,
    BookViewSet,
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'series', SeriesViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
