from django import forms
from .models import Book


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pub_date', 'ISBN_number', 'number_of_pages', 'URL_to_book_cover', 'book_language')

    def clean_ISBN_number(self):
        ISBN_number = self.cleaned_data.get('ISBN_number', )
        if len(ISBN_number) != 13:
            raise forms.ValidationError("ISBN number must be thirteen-digit number")
        return ISBN_number
