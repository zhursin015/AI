import json
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book

# Gemini API кілтің
API_KEY = "AIzaSyBp_6Pw0tDSm_RSMpMXvsVWj27JiuOO7Hg"
genai.configure(api_key=API_KEY)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/index.html', {'books': books})


@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get("message")

            # 1. Қолжетімді модельдерді автоматты түрде іздеу
            available_models = [m.name for m in genai.list_models() if
                                'generateContent' in m.supported_generation_methods]

            # 2. Ең қолайлы модельді таңдау (тізімнен біріншісін немесе flash-ты)
            selected_model = 'gemini-1.5-flash'  # Әдепкі бойынша
            if available_models:
                # Тізімде 'models/' деген префикс болуы мүмкін, соны қолданамыз
                selected_model = available_models[0]

                # 3. ИИ жауабын алу
            model = genai.GenerativeModel(selected_model)
            response = model.generate_content(user_query)

            return JsonResponse({"reply": response.text})

        except Exception as e:
            # Қатені нақты терминалдан көру
            print(f"ERROR: {str(e)}")
            return JsonResponse({"reply": f"🤖 Қате: {str(e)}. Модель табылмады немесе лимит бітті."})

    return JsonResponse({"reply": "Error"}, status=400)
