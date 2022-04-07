from django.shortcuts import render, get_object_or_404
from .forms import AddBookForm
from .models import Book
from django.contrib.postgres.search import SearchVector
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
class AddEditBookDone(TemplateView):
    template_name = "book_app/Library/add_edit_book_done.html"


class BookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'book_app/Library/book_list.html'
    model = Book

    def get(self, request, **kwargs):
        searchfield = request.GET.get('searchfield')
        fromdate = request.GET.get('fromdate')
        todate = request.GET.get('todate')

        if searchfield is None and fromdate is None and todate is None:
            search = self.queryset

        elif searchfield == '':
            search = Book.objects.annotate(search=SearchVector('title', 'author', 'book_language'), ) \
                .filter(pub_date__range=(fromdate, todate))
        else:
            search = Book.objects.annotate(search=SearchVector('title', 'author', 'book_language'), ) \
                .filter(search=searchfield) \
                .filter(pub_date__range=(fromdate, todate))
        paginator = Paginator(search, 10)
        page = request.GET.get('page')
        try:
            display_list = paginator.page(page)
        except PageNotAnInteger:
            display_list = paginator.page(1)
        except EmptyPage:
            display_list = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'books': display_list,
                                                    "page_obj": display_list})


class BookCreateView(CreateView):
    queryset = Book.objects.all()
    template_name = 'book_app/Library/add_edit_book.html'
    form_class = AddBookForm
    success_url = reverse_lazy('create_done')


class BookUpdateView(UpdateView):
    queryset = Book.objects.all()
    template_name = 'book_app/Library/add_edit_book.html'
    form_class = AddBookForm
    success_url = reverse_lazy('update_done')

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(Book, id=id)
