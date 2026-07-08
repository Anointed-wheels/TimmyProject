from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot import library_ai_response

@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")
            
            # Get response from our Gemini-powered chatbot
            response = library_ai_response(message)
            
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
            
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


# 08072573389