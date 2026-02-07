from django.views.generic import TemplateView
from .models import Book


class BookListView(TemplateView):
    template_name = 'books/book_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.select_related('author', 'genre', 'publisher', 'series').all()
        return context
