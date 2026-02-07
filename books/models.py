from django.db import models


class Author(models.Model):
    full_name = models.TextField('ФИО')
    biography = models.TextField('Биография')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.TextField('Название')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.TextField('Название')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.TextField('Название')

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.TextField('Название')
    year = models.PositiveIntegerField('Год издания', null=True)
    description = models.TextField('Описание')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Автор'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Жанр'
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books',
        verbose_name='Серия'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Издательство'
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
