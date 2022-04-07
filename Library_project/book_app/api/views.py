from rest_framework import generics
from ..models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic.base import View, TemplateView
from django.shortcuts import render
import requests


class BookListApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'title': ['exact'], 'author': ['exact'], 'book_language': ['exact'], 'pub_date': ['range']}


class BookDetailApiView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookFromGoogle(View):
    model = Book
    template_name = 'book_app/Library/import_book.html'

    @staticmethod
    def get_api_books_from_google(i, title='', author=''):
        query = ''
        if title != '' and author != '':
            query = 'intitle:' + title + '+' + 'inauthor:' + author
        elif title == '':
            query = 'inauthor:' + author
        elif author == '':
            query = 'intitle:' + title

        params = {"q": query}
        url = 'https://www.googleapis.com/books/v1/volumes'
        response = requests.get(url, params=params)
        response_dict = response.json()

        return response_dict['items'][i]['volumeInfo'], response_dict['items']

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title_field = request.POST.get('title_field', )
        author_field = request.POST.get('author_field', )
        google_api_books = self.get_api_books_from_google(0, title_field, author_field)

        for i in range(len(google_api_books[1])):
            google_api_books = self.get_api_books_from_google(i, title_field, author_field)
            try:
                new_book = Book(title=self.check_field_exist_in_api_data(google_api_books[0],
                                                                         'title'),
                                author=self.check_field_exist_in_api_data(google_api_books[0],
                                                                          'authors'),
                                pub_date=self.check_field_exist_in_api_data(google_api_books[0],
                                                                            'publishedDate'),
                                ISBN_number=self.check_field_exist_in_api_data(google_api_books[0],
                                                                               'industryIdentifiers'),
                                number_of_pages=self.check_field_exist_in_api_data(google_api_books[0],
                                                                                   'pageCount'),
                                URL_to_book_cover=self.check_field_exist_in_api_data(google_api_books[0],
                                                                                     'canonicalVolumeLink'),
                                book_language=self.check_field_exist_in_api_data(google_api_books[0],
                                                                                 'language'),
                                )
                check_book_exist = Book.objects.filter(title=new_book.title, ISBN_number=new_book.ISBN_number).exists()
                if not check_book_exist:
                    new_book.save()
                else:
                    continue
            except KeyError:
                print('Key or value propably doesn\'t exist in current match: ')
                continue

        return render(request, "book_app/Library/import_view_done.html")

    def check_field_exist_in_api_data(self, items_volumeInfo_data, final_field):
        final_fields = ['publishedDate', 'industryIdentifiers', 'authors',
                        'language', 'pagecount', 'canonicalVolumeLink']
        list_of_checking_function = [self.check_date, self.check_ISBN_is_13, self.check_author_quantity,
                                     self.check_language, self.check_page_count, self.check_url]
        if final_field in items_volumeInfo_data:
            for el in range(len(final_fields)):
                if final_field in final_fields[el]:
                    return list_of_checking_function[el](items_volumeInfo_data, final_field)
            return items_volumeInfo_data[final_field]
        elif final_field not in items_volumeInfo_data:
            return None

    @staticmethod
    def check_date(data, field):
        if len(data[field]) <= 4:  # if pub_date has only 4 digit
            return data[field] + '-01-01'
        elif len(data[field]) <= 7:  # if pub_date has only 4 digit
            return data[field] + '-01'
        else:
            return data[field]

    @staticmethod
    def check_ISBN_is_13(data, field):
        for index in range(len(data[field])):
            if data[field][index]['type'] == 'ISBN_13':
                return data[field][index]['identifier']
            elif data[field][index]['type'] != 'ISBN_13':
                continue
        else:
            return data[field][0]['identifier']

    @staticmethod
    def check_author_quantity(data, field):
        author_list = ''
        for author in data[field]:
            if len(data[field]) > 1:
                author_list += author
                author_list += ', '
            elif len(data[field]) == 1:
                author_list += author

        return author_list

    @staticmethod
    def check_page_count(data, field):
        return data[field]

    @staticmethod
    def check_url(data, field):
        return data[field]

    @staticmethod
    def check_language(data, field):
        return data[field]


class ImportViewDone(TemplateView):
    template_name = "book_app/Library/import_view_done.html"
