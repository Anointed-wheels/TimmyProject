from django.http import JsonResponse
import json
from .chatbot import library_ai_response

def ai_chat(request):

    if request.method == "POST":
        data = json.loads(request.body)

        message = data.get("message")

        response = library_ai_response(message)

        return JsonResponse({"response": response})