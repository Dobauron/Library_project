from rest_framework.test import APITestCase
from ..models import Book
from ..api.serializers import BookSerializer


class TestSerializers(APITestCase):
    def setUp(self):
        self.new_book = Book.objects.create(
            title='hobbit homecoming',
            author='tolkien',
            pub_date='2022-08-09',
            number_of_pages='456',
            ISBN_number='23564523454',
            URL_to_book_cover='www.gooogle.com',
            book_language='pl'

        )

        self.serializer = BookSerializer(instance=self.new_book)
        self.data = self.serializer.data

    def test_serialization(self):
        valid_dict = {'title': 'starwars', 'author': 'lucas arts'}
        serializer = BookSerializer(data=valid_dict)
        self.assertTrue(serializer.is_valid())

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.data.keys()),
                         {'id', 'title', 'author', 'pub_date', 'number_of_pages', 'ISBN_number', 'URL_to_book_cover',
                          'book_language'})

    def test_number_of_pages_field_data_type(self):
        self.assertEqual(type(self.data['number_of_pages']), int)
