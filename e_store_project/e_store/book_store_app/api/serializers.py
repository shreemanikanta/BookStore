from rest_framework import serializers
from book_store_app.models import Books, Language


class AddBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = [
                'title', 'description', 'author', 'quantity', 'price', 'image'
                ]


class BookLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['name']


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = [
                'id', 'title', 'description', 'author',
                'added_quantity', 'quantity', 'price', 'image'
                ]


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'
