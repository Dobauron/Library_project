from django.test import TestCase
from ..models import Book
import datetime


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(author='tolkien', title='hobbit', pub_date='2000-03-06', URL_to_book_cover='www.google.com')

    def setUp(self):
        self.fields = ['title', "author", 'pub_date', "ISBN_number",
                       "number_of_pages", "URL_to_book_cover",
                       'book_language']
        self.book = Book.objects.get(id=1)

    def test_get_absolute_url(self):

        self.assertEqual(self.book.get_absolute_url(), '/library/update/1')

    def test_book_title_name_label(self):
        field_label = self.book._meta.get_field(self.fields[0]).verbose_name
        self.assertEqual(field_label, self.fields[0])

    def test_book_title_max_length(self):
        max_length = self.book._meta.get_field(self.fields[0]).max_length
        self.assertEqual(max_length, 150)

    def test_book_author_name_label(self):
        field_label = self.book._meta.get_field(self.fields[1]).verbose_name
        self.assertEqual(field_label, self.fields[1])

    def test_book_author_max_length(self):
        max_length = self.book._meta.get_field(self.fields[1]).max_length
        self.assertEqual(max_length, 250)

    def test_book_pub_date_name_label(self):
        field_label = self.book._meta.get_field(self.fields[2]).verbose_name
        self.assertEqual(field_label, 'pub date')

    def test_book_pub_date_value(self):
        self.assertEqual(self.book.pub_date, datetime.date(2000, 3, 6))

    def test_book_ISBN_number_name_label(self):
        field_label = self.book._meta.get_field(self.fields[3]).verbose_name
        self.assertEqual(field_label, 'ISBN number')

    def test_book_ISBN_number_max_length(self):
        max_length = self.book._meta.get_field(self.fields[3]).max_length
        self.assertEqual(max_length, 30)

    def test_book_number_of_pages_name_label(self):
        field_label = self.book._meta.get_field(self.fields[4]).verbose_name
        self.assertEqual(field_label, 'number of pages')

    def test_book_number_of_pages_value(self):
        self.assertEqual(self.book.number_of_pages, None)

    def test_book_URL_to_book_cover_name_label(self):
        field_label = self.book._meta.get_field(self.fields[5]).verbose_name
        self.assertEqual(field_label, 'URL to book cover')

    def test_book_URL_to_book_cover_value(self):
        self.assertEqual(self.book.URL_to_book_cover, 'www.google.com')

    def test_book_language_name_label(self):
        field_label = self.book._meta.get_field(self.fields[6]).verbose_name
        self.assertEqual(field_label, 'book language')

    def test_book_language_value(self):
        self.assertEqual(self.book.book_language, None)

    def test_book_language_length(self):
        max_length = self.book._meta.get_field(self.fields[6]).max_length
        self.assertEqual(max_length, 15)