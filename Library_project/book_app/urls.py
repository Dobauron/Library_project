from django.urls import path, include
from . import views

urlpatterns = [
    path('library/', views.book_list, name='library'),
    path('library/create/', views.BookCreateView.as_view(), name='create'),
    path('library/create/done', views.AddEditBookDone.as_view(), name='create_done'),
    path('library/update/<int:id>/', views.BookUpdateView.as_view(), name='update'),
    path('library/update/<int:id>/done', views.AddEditBookDone.as_view(), name='update_done'),
    path('library/api/', include('book_app.api.urls', namespace='api'))
]