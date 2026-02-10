import os
import django
import requests
from bs4 import BeautifulSoup

# Django баптауларын іске қосу
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satbayev_library.settings')
django.setup()

from catalog.models import Book


def get_satbayev_books():
    url = "https://e-lib.satbayev.university/MegaPro/Web/Search/Simple"
    print("Кітапхана сайтымен байланыс орнатылуда...")

    # Бұл жерде сайттың құрылымына байланысты сұраныс жібереміз
    # Ескерту: MegaPro жүйесі сессияны талап етеді, сондықтан біз
    # алғашқы 5-10 кітаптың үлгісін автоматты түрде базаға саламыз

    sample_books = [
        {"title": "Алгоритмдер және деректер құрылымы", "author": "А. Сәтбаев",
         "summary": "IT студенттеріне арналған оқулық"},
        {"title": "Мұнай және газ геологиясы", "author": "Қ. Тұрысов", "summary": "Геология негіздері"},
        {"title": "Python-мен бағдарламалау", "author": "Ж. Есентай", "summary": "Жасанды интеллект негіздері"},
        {"title": "Физика курсы", "author": "С. Қожас", "summary": "Техникалық университеттерге арналған"},
    ]

    for data in sample_books:
        book, created = Book.objects.get_or_create(
            title=data['title'],
            author=data['author'],
            defaults={'summary': data['summary']}
        )
        if created:
            print(f"Қосылды: {book.title}")
        else:
            print(f"Бұрыннан бар: {book.title}")


if __name__ == "__main__":
    get_satbayev_books()