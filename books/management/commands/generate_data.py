from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from books.models import Author, Genre, Series, Publisher, Book
from datetime import datetime
import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        user, created = User.objects.get_or_create(
            username='user1',
            defaults={
                'is_staff': False,
            }
        )
        if created:
            user.set_password('user1')
            user.save()

        
        

        authors_to_create = []
        for _ in range(500):
            authors_to_create.append(Author(
                full_name=fake.name(),
                biography=fake.text(max_nb_chars=200),
                user=user
            ))
        Author.objects.bulk_create(authors_to_create, ignore_conflicts=True)
        
        genres_to_create = []
        genre_names = set()
        while len(genre_names) < 25:
            genre_names.add(fake.word().capitalize())
        for name in genre_names:
            genres_to_create.append(Genre(
                name=name,
                description=fake.text(max_nb_chars=100),
                user=user
            ))
        Genre.objects.bulk_create(genres_to_create, ignore_conflicts=True)
        
        series_to_create = []
        series_names = set()
        while len(series_names) < 25:
            series_names.add(fake.sentence(nb_words=3).rstrip('.').title())
        for name in series_names:
            series_to_create.append(Series(
                name=name,
                description=fake.text(max_nb_chars=150),
                user=user
            ))
        Series.objects.bulk_create(series_to_create, ignore_conflicts=True)
        
        publishers_to_create = []
        publisher_names = set()
        while len(publisher_names) < 30:
            publisher_names.add(fake.company())
        for name in publisher_names:
            publishers_to_create.append(Publisher(
                name=name,
                description=fake.text(max_nb_chars=100),
                user=user
            ))
        Publisher.objects.bulk_create(publishers_to_create, ignore_conflicts=True)
        

        authors_list = list(Author.objects.all())
        genres_list = list(Genre.objects.all())
        series_list = list(Series.objects.all())
        publishers_list = list(Publisher.objects.all())
        
        
        total_books = 1000
        books_to_create = []
        
    
        books_created_in_series = 0
        author_index = 0
        
        for series in series_list:
            books_in_this_series = random.randint(2, 7)
            
            for _ in range(books_in_this_series):
                if random.random() < 0.9:
                    year = random.randint(1800, 2026)
                else:

                    year = random.randint(1000, datetime.now().year) if random.random() > 0.1 else None
                
                author = authors_list[author_index % len(authors_list)]
                author_index += 1
                
                books_to_create.append(Book(
                    title=fake.sentence(nb_words=4).rstrip('.').title(),
                    year=year,
                    description=fake.text(max_nb_chars=300),
                    author=author,
                    genre=random.choice(genres_list),
                    series=series,
                    publisher=random.choice(publishers_list),
                    user=user
                ))
                books_created_in_series += 1
        
        books_without_series = total_books - books_created_in_series
        

        for i in range(books_without_series):
            if random.random() < 0.9:
                year = random.randint(1800, 2026)
            else:
                year = random.randint(1000, datetime.now().year) if random.random() > 0.1 else None
            
            author = authors_list[author_index % len(authors_list)]
            author_index += 1
            
            books_to_create.append(Book(
                title=fake.sentence(nb_words=4).rstrip('.').title(),
                year=year,
                description=fake.text(max_nb_chars=300),
                author=author,
                genre=random.choice(genres_list),
                series=None,
                publisher=random.choice(publishers_list),
                user=user
            ))
        Book.objects.bulk_create(books_to_create, ignore_conflicts=True)
