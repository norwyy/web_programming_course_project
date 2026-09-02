from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from books.api import AuthorViewSet, BookViewSet, GenreViewSet, SeriesViewSet, PublisherViewSet, AuthViewSet
from books.views import BookListView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="authors")
router.register("genres", GenreViewSet, basename="genres")
router.register("series", SeriesViewSet, basename="series")
router.register("publishers", PublisherViewSet, basename="publishers")
router.register("books", BookViewSet, basename="books")
router.register("auth", AuthViewSet, basename="auth")

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)