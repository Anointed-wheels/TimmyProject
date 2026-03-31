from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import BorrowRecord
from django.shortcuts import render, redirect, get_object_or_404

from django.core.mail import send_mail
from django.conf import settings


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
from django.utils.timezone import now

@login_required
def my_borrows(request):

    records = BorrowRecord.objects.filter(user=request.user)

    for r in records:
        if r.status == "approved":

            days_left = (r.due_date - now()).days

            if days_left in [3, 2, 1]:
                send_mail(
                    "Return Reminder",
                    f"{r.book.title} is due in {days_left} day(s)",
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email]
                )

            if r.due_date < now():
                days_late = (now() - r.due_date).days
                r.fine = days_late * 50
                r.save()

    read_books = ReadHistory.objects.filter(
        user=request.user
    ).values_list("book_id", flat=True)

    return render(request, "borrow/my_borrows.html", {
        "records": records,
        "read_books": read_books
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

    send_mail(
        "Book Returned",
        f"You have returned {record.book.title}",
        settings.DEFAULT_FROM_EMAIL,
        [record.user.email]
    )

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

    if record.status != "pending":
        return redirect("approve_requests")

    send_mail(
        "Book Approved",
        f"Your request for {record.book.title} has been approved",
        settings.DEFAULT_FROM_EMAIL,
        [record.user.email]
    )

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

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BorrowRecord

@login_required
def cancel_request(request, request_id):   # ✅ MUST MATCH URL

    record = get_object_or_404(
        BorrowRecord,
        id=request_id,
        user=request.user   # 🔒 user can only cancel their own request
    )

    if record.status == "pending":
        record.status = "cancelled"
        record.save()
        messages.success(request, "Request cancelled successfully")

    else:
        messages.error(request, "You cannot cancel this request")

    return redirect("my_borrows")   # change to your page name


from .models import BorrowRecord, ReadHistory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def mark_as_read(request, record_id):

    record = get_object_or_404(
        BorrowRecord,
        id=record_id,
        user=request.user,
        status="approved"   # ✅ ONLY approved allowed
    )

    # Prevent duplicate entries
    if not ReadHistory.objects.filter(user=request.user, book=record.book).exists():

        ReadHistory.objects.create(
            user=request.user,
            book=record.book
        )

    messages.success(request, "Book marked as read")
    return redirect("my_borrows")



from django.db.models import Q

@login_required
def toggle_read(request, record_id):

    record = get_object_or_404(
        BorrowRecord,
        id=record_id,
        user=request.user
    )

    # ✅ Allow ONLY approved or returned
    if record.status not in ["approved", "returned"]:
        messages.error(request, "You cannot mark this book as read")
        return redirect("my_borrows")

    existing = ReadHistory.objects.filter(
        user=request.user,
        book=record.book
    )

    # ✅ TOGGLE LOGIC
    if existing.exists():
        existing.delete()
        messages.success(request, "Marked as unread")
    else:
        ReadHistory.objects.create(
            user=request.user,
            book=record.book
        )
        messages.success(request, "Marked as read")

    return redirect("my_borrows")

    
from django.core.paginator import Paginator

@login_required
def read_history(request):
    history = ReadHistory.objects.filter(user=request.user)

    paginator = Paginator(history, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "borrow/read_history.html", {
        "page_obj": page_obj
    })