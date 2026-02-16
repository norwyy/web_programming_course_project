from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    AuthorViewSet,
    GenreViewSet,
    SeriesViewSet,
    PublisherViewSet,
    BookViewSet,
)
from .auth_api import current_user, login_view, logout_view

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'series', SeriesViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/current-user/', current_user, name='current-user'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
]
