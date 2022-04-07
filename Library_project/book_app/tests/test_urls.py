from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import BookListView, BookCreateView, AddEditBookDone, BookUpdateView
from ..api.views import BookListApiView, BookDetailApiView, BookFromGoogle, ImportViewDone


class TestUrls(SimpleTestCase):

    def test_Library_url_resolves(self):
        url = reverse('library')
        self.assertEqual(resolve(url).func.view_class, BookListView)

    def test_Create_url_resolves(self):
        url = reverse('create')
        self.assertEqual(resolve(url).func.view_class, BookCreateView)

    def test_Update_url_resolves(self):
        url = reverse('update', args=[0])
        self.assertEqual(resolve(url).func.view_class, BookUpdateView)

    def test_UpdatedDone_url_resolves(self):
        url = reverse('update_done', args=[0])
        self.assertEqual(resolve(url).func.view_class, AddEditBookDone)


class TestApiUrls(SimpleTestCase):

    def test_BookApiList_url_resolves(self):
        url = reverse('api:book_api_list')
        self.assertEqual(resolve(url).func.view_class, BookListApiView)

    def test_BookApiDetail_url_resolves(self):
        url = reverse('api:book_api_detail', args=[5])
        self.assertEqual(resolve(url).func.view_class, BookDetailApiView)

    def test_ImportBook_url_resolves(self):
        url = reverse('api:import_book')
        self.assertEqual(resolve(url).func.view_class, BookFromGoogle)

    def test_ImportBookDone_url_resolves(self):
        url = reverse('api:import_book_done')
        self.assertEqual(resolve(url).func.view_class, ImportViewDone)
