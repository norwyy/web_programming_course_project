import json

from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from books.models import Author, Genre, Series, Publisher, Book


class AuthenticatedAPITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password',
        )
        self.client.force_login(self.user)


class AuthorsViewsetTestCase(AuthenticatedAPITestCase):
    def test_get_list(self):
        author = baker.make('books.Author')

        r = self.client.get('/api/authors/')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        assert author.full_name == data[0]['full_name']
        assert author.id == data[0]['id']
        assert author.biography == data[0]['biography']
        assert len(data) == 1

    def test_create_author(self):
        r = self.client.post(
            '/api/authors/',
            data=json.dumps(
                {
                    'full_name': 'Иван Иванов',
                    'biography': 'Биография',
                }
            ),
            content_type='application/json',
        )
        self.assertTrue(200 <= r.status_code < 300)

        authors = Author.objects.all()
        assert len(authors) == 1

        new_author = authors.first()
        assert new_author.full_name == 'Иван Иванов'
        assert new_author.biography == 'Биография'

    def test_delete_author(self):
        authors = baker.make('books.Author', 10)

        r = self.client.get('/api/authors/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert len(data) == 10

        author_id_to_delete = authors[3].id
        r = self.client.delete(f'/api/authors/{author_id_to_delete}/')
        self.assertIn(r.status_code, (200, 204))

        r = self.client.get('/api/authors/')
        data = r.json()
        assert len(data) == 9
        assert author_id_to_delete not in [i['id'] for i in data]

    def test_update_author(self):
        authors = baker.make('books.Author', 10)
        author: Author = authors[2]

        r = self.client.get(f'/api/authors/{author.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data['full_name'] == author.full_name

        r = self.client.put(
            f'/api/authors/{author.id}/',
            data=json.dumps(
                {
                    'full_name': 'Новое имя',
                    'biography': 'Новая биография',
                }
            ),
            content_type='application/json',
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/authors/{author.id}/')
        data = r.json()
        assert data['full_name'] == 'Новое имя'

        author.refresh_from_db()
        assert data['full_name'] == author.full_name


class GenresViewsetTestCase(AuthenticatedAPITestCase):
    def test_get_list(self):
        genre = baker.make('books.Genre')

        r = self.client.get('/api/genres/')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        assert genre.name == data[0]['name']
        assert genre.id == data[0]['id']
        assert len(data) == 1

    def test_create_genre(self):
        r = self.client.post(
            '/api/genres/',
            data=json.dumps(
                {
                    'name': 'Фантастика',
                    'description': 'Описание жанра',
                }
            ),
            content_type='application/json',
        )
        self.assertTrue(200 <= r.status_code < 300)

        genres = Genre.objects.all()
        assert len(genres) == 1

        new_genre = genres.first()
        assert new_genre.name == 'Фантастика'
        assert new_genre.description == 'Описание жанра'

    def test_delete_genre(self):
        genres = baker.make('books.Genre', 10)

        r = self.client.get('/api/genres/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert len(data) == 10

        genre_id_to_delete = genres[3].id
        r = self.client.delete(f'/api/genres/{genre_id_to_delete}/')
        self.assertIn(r.status_code, (200, 204))

        r = self.client.get('/api/genres/')
        data = r.json()
        assert len(data) == 9
        assert genre_id_to_delete not in [i['id'] for i in data]

    def test_update_genre(self):
        genres = baker.make('books.Genre', 10)
        genre: Genre = genres[2]

        r = self.client.get(f'/api/genres/{genre.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data['name'] == genre.name

        r = self.client.put(
            f'/api/genres/{genre.id}/',
            data=json.dumps(
                {
                    'name': 'Детектив',
                    'description': 'Новое описание',
                }
            ),
            content_type='application/json',
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/genres/{genre.id}/')
        data = r.json()
        assert data['name'] == 'Детектив'

        genre.refresh_from_db()
        assert data['name'] == genre.name


class SeriesViewsetTestCase(AuthenticatedAPITestCase):
    def test_get_list(self):
        series = baker.make('books.Series')

        r = self.client.get('/api/series/')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        assert series.name == data[0]['name']
        assert series.id == data[0]['id']
        assert len(data) == 1

    def test_create_series(self):
        r = self.client.post(
            '/api/series/',
            data=json.dumps(
                {
                    'name': 'Серия книг',
                    'description': 'Описание серии',
                }
            ),
            content_type='application/json',
        )
        self.assertTrue(200 <= r.status_code < 300)

        series_qs = Series.objects.all()
        assert len(series_qs) == 1

        new_series = series_qs.first()
        assert new_series.name == 'Серия книг'
        assert new_series.description == 'Описание серии'

    def test_delete_series(self):
        series = baker.make('books.Series', 10)

        r = self.client.get('/api/series/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert len(data) == 10

        series_id_to_delete = series[3].id
        r = self.client.delete(f'/api/series/{series_id_to_delete}/')
        self.assertIn(r.status_code, (200, 204))

        r = self.client.get('/api/series/')
        data = r.json()
        assert len(data) == 9
        assert series_id_to_delete not in [i['id'] for i in data]

    def test_update_series(self):
        series_list = baker.make('books.Series', 10)
        series: Series = series_list[2]

        r = self.client.get(f'/api/series/{series.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data['name'] == series.name

        r = self.client.put(
            f'/api/series/{series.id}/',
            data=json.dumps(
                {
                    'name': 'Другая серия',
                    'description': 'Новое описание',
                }
            ),
            content_type='application/json',
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/series/{series.id}/')
        data = r.json()
        assert data['name'] == 'Другая серия'

        series.refresh_from_db()
        assert data['name'] == series.name


class PublishersViewsetTestCase(AuthenticatedAPITestCase):
    def test_get_list(self):
        publisher = baker.make('books.Publisher')

        r = self.client.get('/api/publishers/')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        assert publisher.name == data[0]['name']
        assert publisher.id == data[0]['id']
        assert len(data) == 1

    def test_create_publisher(self):
        r = self.client.post(
            '/api/publishers/',
            data=json.dumps({'name': 'Издательство'}),
            content_type='application/json',
        )
        self.assertTrue(200 <= r.status_code < 300)

        publishers = Publisher.objects.all()
        assert len(publishers) == 1

        new_publisher = publishers.first()
        assert new_publisher.name == 'Издательство'

    def test_delete_publisher(self):
        publishers = baker.make('books.Publisher', 10)

        r = self.client.get('/api/publishers/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert len(data) == 10

        publisher_id_to_delete = publishers[3].id
        r = self.client.delete(f'/api/publishers/{publisher_id_to_delete}/')
        self.assertIn(r.status_code, (200, 204))

        r = self.client.get('/api/publishers/')
        data = r.json()
        assert len(data) == 9
        assert publisher_id_to_delete not in [i['id'] for i in data]

    def test_update_publisher(self):
        publishers = baker.make('books.Publisher', 10)
        publisher: Publisher = publishers[2]

        r = self.client.get(f'/api/publishers/{publisher.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data['name'] == publisher.name

        r = self.client.put(
            f'/api/publishers/{publisher.id}/',
            data=json.dumps({'name': 'Новое издательство'}),
            content_type='application/json',
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/publishers/{publisher.id}/')
        data = r.json()
        assert data['name'] == 'Новое издательство'

        publisher.refresh_from_db()
        assert data['name'] == publisher.name


class BooksViewsetTestCase(AuthenticatedAPITestCase):
    def test_get_list(self):
        author = baker.make('books.Author')
        genre = baker.make('books.Genre')
        publisher = baker.make('books.Publisher')
        book = baker.make(
            'books.Book',
            author=author,
            genre=genre,
            publisher=publisher,
        )

        r = self.client.get('/api/books/')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        item = data[0]
        assert book.title == item['title']
        assert book.id == item['id']
        assert book.author.id == item['author']['id']
        assert book.author.full_name == item['author']['full_name']
        assert book.genre.id == item['genre']['id']
        assert book.publisher.id == item['publisher']['id']
        assert len(data) == 1

    def test_create_book(self):
        author = baker.make('books.Author')
        genre = baker.make('books.Genre')
        publisher = baker.make('books.Publisher')

        r = self.client.post(
            '/api/books/',
            data=json.dumps(
                {
                    'title': 'Название книги',
                    'year': 2020,
                    'description': 'Описание',
                    'author': author.id,
                    'genre': genre.id,
                    'publisher': publisher.id,
                    'series': None,
                }
            ),
            content_type='application/json',
        )
        self.assertTrue(200 <= r.status_code < 300)

        books = Book.objects.all()
        assert len(books) == 1

        new_book = books.first()
        assert new_book.title == 'Название книги'
        assert new_book.author == author
        assert new_book.genre == genre
        assert new_book.publisher == publisher

    def test_delete_book(self):
        books = baker.make('books.Book', 10)

        r = self.client.get('/api/books/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert len(data) == 10

        book_id_to_delete = books[3].id
        r = self.client.delete(f'/api/books/{book_id_to_delete}/')
        self.assertIn(r.status_code, (200, 204))

        r = self.client.get('/api/books/')
        data = r.json()
        assert len(data) == 9
        assert book_id_to_delete not in [i['id'] for i in data]

    def test_update_book(self):
        books = baker.make('books.Book', 10)
        book: Book = books[2]

        r = self.client.get(f'/api/books/{book.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data['title'] == book.title

        r = self.client.put(
            f'/api/books/{book.id}/',
            data=json.dumps(
                {
                    'title': 'Обновлённое название',
                    'year': book.year,
                    'description': book.description,
                    'author': book.author.id,
                    'genre': book.genre.id,
                    'publisher': book.publisher.id,
                    'series': book.series.id if book.series else None,
                }
            ),
            content_type='application/json',
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/books/{book.id}/')
        data = r.json()
        assert data['title'] == 'Обновлённое название'

        book.refresh_from_db()
        assert data['title'] == book.title
