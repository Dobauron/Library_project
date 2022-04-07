from django.test import TestCase
from ..forms import AddBookForm


class AddBookFormTest(TestCase):
    def setUp(self):
        self.form = AddBookForm(data={
            'author': 'tolkien',
            'title': 'hobbit',
            'pub_date': '2000-03-06',
            'ISBN_number': '0987654321098',
            'number_of_pages': '456',
            'URL_to_book_cover': 'www.google.com',
            'book_language': 'pl'
        })

    def test_add_book_form_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_add_book_form_no_data(self):
        form = AddBookForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)

    def test_clean_ISBN_number(self):
        self.assertTrue(self.form.clean_ISBN_number, "ISBN number must be thirteen-digit number")
