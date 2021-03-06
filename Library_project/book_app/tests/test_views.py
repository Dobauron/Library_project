from django.test import TestCase, Client
from django.urls import reverse
from ..models import Book
from rest_framework.test import APITestCase
from rest_framework import status


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.library_url = reverse('library')
        self.create_url = reverse('create')
        self.create_done_url = reverse('create_done')
        self.update_done_url = reverse('update_done', args=[0])
        self.new_book = Book.objects.create(
            title='hobbit homecoming',
            author='tolkien',
            pub_date='2022-08-09',
            number_of_pages='456',
            ISBN_number='23564523454',
            URL_to_book_cover='www.gooogle.com',
            book_language='pl'

        )
        self.update_url = reverse('update', kwargs={'id': self.new_book.id, })

    def test_csrf_client(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_database_field_compatibility(self):
        self.assertEqual(self.new_book.author, "tolkien")
        self.assertEqual(self.new_book.book_language, 'pl')

    def test_library_GET(self):
        response = self.client.get(self.library_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_app/Library/book_list.html')

    def test_create_GET(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_app/Library/add_edit_book.html')

    def test_create_done_GET(self):
        response = self.client.get(self.create_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_app/Library/add_edit_book_done.html')

    def test_update_GET(self):
        response = self.client.get(self.update_url, {self.new_book.title: 'hobbit'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_app/Library/add_edit_book.html')

    def test_update_done_GET(self):
        response = self.client.get(self.update_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_app/Library/add_edit_book_done.html')

    def test_Library_create_POST_book_record(self):
        response = self.client.post(self.create_url, {
            'title': 'Star Wars',
            'author': 'Lucas Arts',
            'pub_date': '08-7-2000',
            'number_of_pages': 456,
            'ISBN_number': '5235642341223',
            'URL_to_book_cover': 'https://www.google.com/search?channel=fs&client=ubuntu&q=hobbit',
            'book_language': 'pl'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'book_app/Library/add_edit_book.html')
        self.assertRedirects(response, 'create_done')

    def test_Library_update_POST_book_record(self):
        response = self.client.post(reverse('update', kwargs={'id': self.new_book.id}),
                                    {
                                        'title': 'hobbit far away from home',
                                        'author': 'tolkien',
                                        'pub_date': '2022-08-09',
                                        'number_of_pages': 456,
                                        'ISBN_number': '23564523453',
                                        'URL_to_book_cover': 'www.gooogle.com',
                                        'book_language': 'pl'
                                    }, )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.new_book.title, 'hobbit far away from home')
        self.assertRedirects(response, 'update_done')
        self.assertTemplateUsed(response, 'book_app/Library/add_edit_book.html')


class TestApiViews(APITestCase):

    def setUp(self):
        self.new_book = Book.objects.create(
            title='hobbit',
            author='tolkien',
            pub_date='2022-08-09',
            number_of_pages='456',
            ISBN_number='23564523454',
            URL_to_book_cover='www.gooogle.com',
            book_language='pl'

        )
        self.book_api_list_url = reverse('api:book_api_list')
        self.book_api_detail_url = reverse('api:book_api_detail', kwargs={'pk': self.new_book.pk})
        self.import_book_url = reverse('api:import_book')
        self.import_book_done_url = reverse('api:import_book_done')

    def test_book_list_api_view_get(self):
        response = self.client.get(self.book_api_list_url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list_api_view_post(self):
        response = self.client.post(self.book_api_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_detail_api_view_get(self):
        response = self.client.get(self.book_api_detail_url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_detail_api_view_post(self):
        response = self.client.post(self.book_api_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_import_api_view_get(self):
        response = self.client.get(self.import_book_url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_import_api_view_post(self):
        data = {'title_field': 'hobbit', 'author_field': 'tolkien'}
        response = self.client.post(self.import_book_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_import_api_done_view_get(self):
        response = self.client.get(self.import_book_done_url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
