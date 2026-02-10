from django.db import models
from django.contrib.auth.models import User  # Django-ның дайын студенттер базасы


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    is_available = models.BooleanField(default=True)  # Кітап бос па немесе біреуде ме?

    def __str__(self):
        return self.title


class Booking(models.Model):
    # Студент пен кітапты байланыстыру
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Кітап")

    # Күндерді бақылау
    booked_at = models.DateTimeField(auto_now_add=True, verbose_name="Брондалған уақыт")
    return_date = models.DateField(null=True, blank=True, verbose_name="Қайтару күні")

    # Статус
    STATUS_CHOICES = [
        ('reserved', 'Брондалды'),
        ('issued', 'Берілді'),
        ('returned', 'Қайтарылды'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')

    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({self.status})"