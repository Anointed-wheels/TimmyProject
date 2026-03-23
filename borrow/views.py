from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import BorrowRecord
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def request_borrow(request, book_id):

    book = Book.objects.get(id=book_id)

    if book.available_copies > 0:

        BorrowRecord.objects.create(
            user=request.user,
            book=book
        )

    return redirect("homepage")


@login_required
def approve_borrow(request, borrow_id):

    record = BorrowRecord.objects.get(id=borrow_id)

    if not record.approved:

        record.approved = True
        record.book.available_copies -= 1

        record.book.save()
        record.save()

    return redirect("dashboard")


@login_required
def return_book(request, borrow_id):

    record = BorrowRecord.objects.get(id=borrow_id)

    if not record.returned:

        record.returned = True
        record.book.available_copies += 1

        record.book.save()
        record.save()

    return redirect("dashboard")


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import BorrowRecord, Reservation
from django.utils import timezone
from datetime import timedelta

@login_required
def borrow_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    # prevent duplicate request
    if BorrowRecord.objects.filter(user=request.user, book=book, status="pending").exists():
        return redirect("homepage")

    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        due_date=timezone.now() + timedelta(days=7)
    )

    return redirect("my_borrows")



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from books.models import Book
from .models import BorrowRecord

# =========================
# USER REQUEST BOOK
# =========================
@login_required
def request_borrow(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    # prevent duplicate request
    if BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        status="pending"
    ).exists():
        return redirect("book_detail", book_id=book.id)

    BorrowRecord.objects.create(
        user=request.user,
        book=book
    )

    return redirect("my_borrows")


# =========================
# USER DASHBOARD (MY BORROWS)
# =========================
@login_required
def my_borrows(request):

    records = BorrowRecord.objects.filter(
        user=request.user
    ).order_by("-borrow_date")

    # calculate fine
    for r in records:
        if r.status == "approved" and r.due_date < now():
            days = (now() - r.due_date).days
            r.fine = days * 50
            r.save()

    return render(request, "borrow/my_borrows.html", {
        "records": records
    })


# =========================
# ADMIN VIEW REQUESTS
# =========================
@login_required
def manage_requests(request):

    if request.user.user_type not in ["admin", "librarian"]:
        return redirect("homepage")

    status_filter = request.GET.get("status")

    requests = BorrowRecord.objects.all().order_by("-borrow_date")

    if status_filter:
        requests = requests.filter(status=status_filter)

    return render(request, "borrow/manage_requests.html", {
        "requests": requests
    })


# =========================
# APPROVE
# =========================
@login_required
def approve_request(request, request_id):

    record = get_object_or_404(BorrowRecord, id=request_id)

    if record.book.available_copies > 0:
        record.status = "approved"
        record.book.available_copies -= 1

        record.book.save()
        record.save()

    return redirect("manage_requests")


# =========================
# REJECT
# =========================
@login_required
def reject_request(request, request_id):

    record = get_object_or_404(BorrowRecord, id=request_id)

    record.status = "rejected"
    record.save()

    return redirect("manage_requests")


# =========================
# RETURN BOOK (ADMIN/LIBRARIAN)
# =========================
@login_required
def mark_returned(request, request_id):

    record = get_object_or_404(BorrowRecord, id=request_id)

    if record.status == "approved":
        record.status = "returned"
        record.book.available_copies += 1

        record.book.save()
        record.save()

    return redirect("manage_requests")



@login_required
def approve_borrow(request, id):

    record = get_object_or_404(BorrowRecord, id=id)

    if record.book.available_copies > 0:
        record.status = "approved"
        record.book.available_copies -= 1
        record.book.save()
        record.save()

    return redirect("approve_requests")


@login_required
def approve_borrow(request, id):

    record = get_object_or_404(BorrowRecord, id=id)

    if record.book.available_copies > 0:
        record.status = "approved"
        record.book.available_copies -= 1
        record.book.save()
        record.save()

    return redirect("approve_requests")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import DeliveryRequest


@login_required
def request_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        DeliveryRequest.objects.create(
            user=request.user,
            book=book,
            address=address,
            phone=phone
        )

        return redirect("dashboard")

    return render(request, "borrow/request_book.html", {"book": book})

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    DeliveryRequest.objects.create(
        user=request.user,
        book=book,
        address="Reserved (Walk-in)",
        phone="N/A",
        status="pending"
    )

    return redirect("dashboard")