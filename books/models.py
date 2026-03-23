from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Book(models.Model):

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(blank=True, null=True)

    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title