from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='book_covers/', null=True, blank=True)  # ImageField to store book cover images

    def __str__(self):
        return self.title
    


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Linked to the Book model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linked to the User model
    due_date = models.DateField()  # Due date for the book return
    return_date = models.DateField(null=True, blank=True)  # Return date, null means not yet returned
    is_returned = models.BooleanField(default=False)  # Flag to check if book is returned

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    def is_overdue(self):
        """Check if the book is overdue"""
        # Check if the book is overdue and not yet returned
        if self.return_date:
            return self.return_date < timezone.now().date() and not self.is_returned
        return self.due_date < timezone.now().date() and not self.is_returned

    def calculate_fine(self):
        if self.is_overdue():
            overdue_days = (timezone.now().date() - self.due_date).days
            return overdue_days * 1  # Assuming $1 per day fine
        return 0

    def save(self, *args, **kwargs):
        if self.return_date:
            self.is_returned = True  # Automatically mark as returned when return date is set
        super(Loan, self).save(*args, **kwargs)  # Call the parent save method
