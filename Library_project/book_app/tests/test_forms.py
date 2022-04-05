import datetime
from django.test import TestCase
from django.utils import timezone

from ..forms import AddBookForm

class AddBookFormTest(TestCase):
    def test_add_book_form_valid_data(self):
        form = AddBookForm(data={
            'author':'tolkien',
            'title': 'hobbit',
            'pub_date': '2000-03-06',
            'ISBN_number': '0987654321098',
            'number_of_pages': '456',
            'URL_to_book_cover': 'www.google.com',
            'book_language': 'pl'
        })

        self.assertTrue(form.is_valid())

    def test_add_book_form_no_data(self):
        form = AddBookForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),7)