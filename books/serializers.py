from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Genre, Series, Publisher, Book


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'biography', 'picture', 'user']


class GenreSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'user']


class SeriesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Series
        fields = ['id', 'name', 'description', 'user']


class PublisherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description', 'user']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'year', 'description', 'picture',
            'author', 'genre', 'series', 'publisher', 'user'
        ]


class BookWriteSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1000,
        max_value=datetime.now().year
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'year', 'description', 'picture',
            'author', 'genre', 'series', 'publisher', 'user'
        ]


class AuthorStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    top_author_name = serializers.CharField(allow_null=True)
    top_author_name_count = serializers.IntegerField(allow_null=True)


class GenreStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    top_genre_name = serializers.CharField(allow_null=True)
    top_genre_name_count = serializers.IntegerField(allow_null=True)


class SeriesStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()


class PublisherStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()


class BookStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    avg_year = serializers.FloatField(allow_null=True)
    max_year = serializers.IntegerField(allow_null=True)
    min_year = serializers.IntegerField(allow_null=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_superuser']
        read_only_fields = ['id', 'is_superuser']
