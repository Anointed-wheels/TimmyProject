from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from books.models import Book, Category
from django.db.models import Q
from books.ai_recommender import get_book_recommendations

from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .forms import BookForm
import csv, io
from django.contrib import messages
from .forms import CategoryForm

def homepage(request):
    books = Book.objects.all()
    
    # Search
    query = request.GET.get('search')
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        books = books.filter(category__id=category)
    
    # Pagination (20 per page)
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'books': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'page_obj': page_obj,
    }
    return render(request, 'homepage.html', context)


def book_detail(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    recommended_books = get_book_recommendations(book.id)

    context = {
        "book": book,
        "recommended_books": recommended_books
    }

    return render(request, "books/book_detail.html", context)


@login_required
def add_book(request):

    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST.get("title")
        author = request.POST.get("author")
        category_id = request.POST.get("category")
        copies = request.POST.get("copies")

        category = Category.objects.get(id=category_id)

        cover = request.FILES.get("cover")

        Book.objects.create(
            title=title,
            author=author,
            category=category,
            total_copies=copies,
            available_copies=copies,
            cover_image=cover
        )

        messages.success(request,"Book added")

    return render(request,"books/add_book.html",{
        "categories":categories
    })

    if request.FILES.get("csv_file"):

        csv_file = request.FILES["csv_file"]
        category_id = request.POST.get("csv_category")

        category = Category.objects.get(id=category_id)

        decoded = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded)

        next(io_string)

        for row in csv.reader(io_string):

            Book.objects.create(
                title=row[0],
                author=row[1],
                category=category,
                total_copies=row[2],
                available_copies=row[2]
            )




from .models import Category
from django.contrib import messages

@login_required
def add_category(request):

    if request.method == "POST":
        name = request.POST.get("name")

        if Category.objects.filter(name=name).exists():
            messages.error(request, "Category already exists")
        else:
            Category.objects.create(name=name)
            messages.success(request, "Category created")

    categories = Category.objects.all()

    return render(request,"books/add_category.html",{
        "categories":categories
    })

def book_list(request):

    books = Book.objects.all()

    return render(request,"books/book_list.html",{
        "books":books
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category
from django.contrib import messages


def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)
    categories = Category.objects.all()

    if request.method == "POST":

        book.title = request.POST.get("title")
        book.author = request.POST.get("author")

        category_id = request.POST.get("category")
        book.category = Category.objects.get(id=category_id)

        book.total_copies = request.POST.get("copies")

        if request.FILES.get("cover"):
            book.cover_image = request.FILES.get("cover")

        book.save()

        messages.success(request, "Book updated successfully")
        return redirect("book_list")

    return render(request, "books/edit_book.html", {
        "book": book,
        "categories": categories
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from borrow.models import BorrowRecord, Reservation


def books_page(request):

    books = Book.objects.all()

    return render(request, "books/books_page.html", {
        "books": books
    })


from django.db.models import Q

def book_detail(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    recommended_books = Book.objects.filter(
        Q(category=book.category) | Q(author=book.author)
    ).exclude(id=book.id)[:4]

    return render(request, "books/book_detail.html", {
        "book": book,
        "recommended_books": recommended_books
    })