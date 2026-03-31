from django.db import models
from django.conf import settings
from books.models import Book
from django.utils.timezone import now
from datetime import timedelta


from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta

def default_due_date():
    return timezone.now() + timedelta(days=7)

User = get_user_model()

class BorrowRecord(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("returned", "Returned"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=default_due_date)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} - {self.book} ({self.status})"

class Reservation(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    reserved_at = models.DateTimeField(auto_now_add=True)

    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} reserved {self.book}"


class DeliveryRequest(models.Model):

    STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("delivered", "Delivered"),
    )

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)

    address = models.TextField()
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.book}"



from django.db import models
from django.conf import settings
from books.models import Book

User = settings.AUTH_USER_MODEL

class ReadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-read_at']  # latest first

    def __str__(self):
        return f"{self.user} read {self.book}"