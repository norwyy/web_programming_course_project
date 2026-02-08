from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Genre, Series, Publisher, Book


class TestAuthorViewSet(APITestCase):
    def test_list(self):
        baker.make(Author, _quantity=3)
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create(self):
        url = reverse('author-list')
        data = {'full_name': 'Иван Иванов', 'biography': 'Биография'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.first().full_name, data['full_name'])

    def test_retrieve(self):
        author = baker.make(Author)
        url = reverse('author-detail', args=[author.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], author.full_name)

    def test_update(self):
        author = baker.make(Author)
        url = reverse('author-detail', args=[author.pk])
        data = {'full_name': 'Новое имя', 'biography': 'Новая биография'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.full_name, data['full_name'])

    def test_delete(self):
        author = baker.make(Author)
        url = reverse('author-detail', args=[author.pk])
        count_before = Author.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), count_before - 1)
        self.assertFalse(Author.objects.filter(pk=author.pk).exists())


class TestGenreViewSet(APITestCase):
    def test_list(self):
        baker.make(Genre, _quantity=5)
        url = reverse('genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_create(self):
        url = reverse('genre-list')
        data = {'name': 'Фантастика', 'description': 'Описание жанра'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Genre.objects.first().name, data['name'])

    def test_retrieve(self):
        genre = baker.make(Genre)
        url = reverse('genre-detail', args=[genre.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], genre.name)

    def test_update(self):
        genre = baker.make(Genre)
        url = reverse('genre-detail', args=[genre.pk])
        data = {'name': 'Детектив', 'description': 'Новое описание'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        genre.refresh_from_db()
        self.assertEqual(genre.name, data['name'])

    def test_delete(self):
        genre = baker.make(Genre)
        url = reverse('genre-detail', args=[genre.pk])
        count_before = Genre.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), count_before - 1)
        self.assertFalse(Genre.objects.filter(pk=genre.pk).exists())


class TestSeriesViewSet(APITestCase):
    def test_list(self):
        baker.make(Series, _quantity=2)
        url = reverse('series-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        url = reverse('series-list')
        data = {'name': 'Серия книг', 'description': 'Описание серии'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Series.objects.count(), 1)
        self.assertEqual(Series.objects.first().name, data['name'])

    def test_retrieve(self):
        series = baker.make(Series)
        url = reverse('series-detail', args=[series.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], series.name)

    def test_update(self):
        series = baker.make(Series)
        url = reverse('series-detail', args=[series.pk])
        data = {'name': 'Другая серия', 'description': 'Новое описание'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        series.refresh_from_db()
        self.assertEqual(series.name, data['name'])

    def test_delete(self):
        series = baker.make(Series)
        url = reverse('series-detail', args=[series.pk])
        count_before = Series.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Series.objects.count(), count_before - 1)
        self.assertFalse(Series.objects.filter(pk=series.pk).exists())


class TestPublisherViewSet(APITestCase):
    def test_list(self):
        baker.make(Publisher, _quantity=4)
        url = reverse('publisher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create(self):
        url = reverse('publisher-list')
        data = {'name': 'Издательство'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 1)
        self.assertEqual(Publisher.objects.first().name, data['name'])

    def test_retrieve(self):
        publisher = baker.make(Publisher)
        url = reverse('publisher-detail', args=[publisher.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], publisher.name)

    def test_update(self):
        publisher = baker.make(Publisher)
        url = reverse('publisher-detail', args=[publisher.pk])
        data = {'name': 'Новое издательство'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        publisher.refresh_from_db()
        self.assertEqual(publisher.name, data['name'])

    def test_delete(self):
        publisher = baker.make(Publisher)
        url = reverse('publisher-detail', args=[publisher.pk])
        count_before = Publisher.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Publisher.objects.count(), count_before - 1)
        self.assertFalse(Publisher.objects.filter(pk=publisher.pk).exists())


class TestBookViewSet(APITestCase):
    def test_list(self):
        author = baker.make(Author)
        genre = baker.make(Genre)
        publisher = baker.make(Publisher)
        baker.make(Book, author=author, genre=genre, publisher=publisher, _quantity=3)
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create(self):
        author = baker.make(Author)
        genre = baker.make(Genre)
        publisher = baker.make(Publisher)
        url = reverse('book-list')
        data = {
            'title': 'Название книги',
            'year': 2020,
            'description': 'Описание',
            'author': author.pk,
            'genre': genre.pk,
            'publisher': publisher.pk,
            'series': None,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.first()
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.author_id, author.pk)

    def test_retrieve(self):
        author = baker.make(Author)
        genre = baker.make(Genre)
        publisher = baker.make(Publisher)
        book = baker.make(Book, author=author, genre=genre, publisher=publisher)
        url = reverse('book-detail', args=[book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], book.title)
        self.assertEqual(response.data['author']['id'], author.pk)

    def test_update(self):
        author = baker.make(Author)
        genre = baker.make(Genre)
        publisher = baker.make(Publisher)
        book = baker.make(Book, author=author, genre=genre, publisher=publisher)
        url = reverse('book-detail', args=[book.pk])
        data = {
            'title': 'Обновлённое название',
            'year': 2021,
            'description': 'Новое описание',
            'author': author.pk,
            'genre': genre.pk,
            'publisher': publisher.pk,
            'series': None,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, data['title'])

    def test_delete(self):
        author = baker.make(Author)
        genre = baker.make(Genre)
        publisher = baker.make(Publisher)
        book = baker.make(Book, author=author, genre=genre, publisher=publisher)
        url = reverse('book-detail', args=[book.pk])
        count_before = Book.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), count_before - 1)
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())
