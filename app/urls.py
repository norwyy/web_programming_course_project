from django.contrib import admin
from django.urls import path, include
from books.views import BookListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
    path('', BookListView.as_view(), name='book_list'),
]
