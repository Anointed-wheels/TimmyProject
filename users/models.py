from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta
from django.utils import timezone

# Custom user with roles
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('normal', 'Normal User'),
        ('librarian', 'Librarian'),
        ('admin_attendant', 'Admin Attendant'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='normal')
    is_deleted = models.BooleanField(default=False)

    is_suspended = models.BooleanField(default=False)

# Pending user for email verification
class PendingUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)
    otp_created = models.DateTimeField(auto_now_add=True)

    def is_otp_valid(self):
        return timezone.now() < self.otp_created + timedelta(hours=2)