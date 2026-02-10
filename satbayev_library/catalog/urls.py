from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Міне, осы жерде book_list функциясы керек
    path('chat/', views.ai_chat, name='ai_chat'),
]