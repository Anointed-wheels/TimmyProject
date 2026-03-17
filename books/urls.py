from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("add-book/", add_book, name="add_book"),
    path('books/', views.book_list, name='book_list'),
    path('add-category/', add_category, name='add_category'),
    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('', views.books_page, name="books_page"),
    path('book/<int:book_id>/', views.book_detail, name="book_detail"),
    
    # Add book list/detail later
]