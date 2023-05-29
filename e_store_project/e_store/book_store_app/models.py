from django.db import models
from user_app.models import User


class Language(models.Model):
    """
    A model representing a language.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Books(models.Model):
    """
    A class representing books in the bookstore.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    description = models.TextField(max_length=600)
    author = models.CharField(max_length=200)
    added_quantity = models.IntegerField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='books')
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookLanguage(models.Model):
    """
    Model representing the relationship between a book and its language.
    """
    language = models.ForeignKey(Language,
                                 on_delete=models.CASCADE,
                                 related_name='books_languages')
    book = models.ForeignKey(Books,
                             on_delete=models.CASCADE,
                             related_name='books_languages')

    def __str__(self):
        return self.book.title + '  -------  ' + self.language.name
