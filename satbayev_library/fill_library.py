import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satbayev_library.settings')
django.setup()
from catalog.models import Book

books = [
    {"title": "Алгоритмдер және деректер құрылымдары", "author": "Ахметов Б. С.", "summary": "IT мамандықтарына арналған негізгі оқулық."},
    {"title": "Инженерлік графика", "author": "Жаржанов Б. К.", "summary": "Сызба жұмыстары мен дизайн негіздері."},
    {"title": "Мұнай кен орындарын игеру", "author": "Тұрысов Қ. К.", "summary": "Геология және мұнай инженериясы."},
    {"title": "Python-мен деректерді талдау", "author": "Жолдасбай А.", "summary": "Data Science және Machine Learning негіздері."},
    {"title": "Қазақстан тарихы", "author": "Көмеков Б. Е.", "summary": "Университет студенттеріне арналған курс."},
]

for b in books:
    Book.objects.get_or_create(title=b['title'], author=b['author'], defaults={'summary': b['summary']})
print("Базаға 5 маңызды кітап қосылды!")