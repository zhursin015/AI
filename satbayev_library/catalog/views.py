import json
import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book

# Render-дегі Environment Variables бөлімінен кілтті қауіпсіз түрде алу
# Егер ол табылмаса, ескі кілтті уақытша қолданады (бірақ бұл қауіпті)
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBLFvxJgcTfjx3cXZF8VQ8XcNdWnb6gJPU")
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

            # 1. Қолжетімді модельдерді іздеу
            available_models = [m.name for m in genai.list_models() if
                                'generateContent' in m.supported_generation_methods]

            # 2. Модельді таңдау
            # Егер тізімде gemini-1.5-flash болса, соны таңдаймыз, әйтпесе біріншісін
            selected_model = 'models/gemini-1.5-flash' 
            if available_models:
                if 'models/gemini-1.5-flash' in available_models:
                    selected_model = 'models/gemini-1.5-flash'
                else:
                    selected_model = available_models[0]

            # 3. ИИ жауабын алу
            model = genai.GenerativeModel(selected_model)
            response = model.generate_content(user_query)

            return JsonResponse({"reply": response.text})

        except Exception as e:
            print(f"ERROR: {str(e)}")
            # Егер кілт блокталса, осы жерде нақты қате көрінеді
            return JsonResponse({"reply": f"🤖 Қате: {str(e)}. Жаңа API кілтті Render-ге қосуды ұмытпаңыз."})

    return JsonResponse({"reply": "Error"}, status=400)
