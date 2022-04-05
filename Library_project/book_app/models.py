from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=150, null=True)
    author = models.CharField(max_length=250, null=True)
    pub_date = models.DateField(null=True)
    ISBN_number = models.CharField(max_length=30, unique=True, null=True)
    number_of_pages = models.IntegerField(null=True)
    URL_to_book_cover = models.URLField(null=True)
    book_language = models.CharField(max_length=15, null=True)

    def get_absolute_url(self):
        return f'/library/update/{self.id}'

    def __str__(self):
        return f'{self.title, self.author}'
