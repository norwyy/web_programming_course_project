from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from books.api import AuthorViewSet, BookViewSet, GenreViewSet, SeriesViewSet, PublisherViewSet
from books.views import BookListView
from django.conf import settings
from django.conf.urls.static import static
from books.auth_api import current_user, login_view, logout_view

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="authors")
router.register("genres", GenreViewSet, basename="genres")
router.register("series", SeriesViewSet, basename="series")
router.register("publishers", PublisherViewSet, basename="publishers")
router.register("books", BookViewSet, basename="books")

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/current-user/', current_user, name='current-user'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
