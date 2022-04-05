from django.urls import path
from . import views

app_name = 'book_app'
urlpatterns = [
    path('book/', views.BookListApiView.as_view(), name='book_api_list'),
    path('book/<pk>/', views.BookDetailApiView.as_view(), name='book_api_detail'),
    path('import/', views.BookFromGoogle.as_view(), name='import_book'),
    path('import/done', views.ImportViewDone.as_view(), name='import_book_done'),
]