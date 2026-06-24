import os
from google import genai
from google.genai import types
from django.conf import settings

def library_ai_response(user_message):
    try:
        # 1. Initialize the client (it automatically picks up GEMINI_API_KEY from environment)
        client = genai.Client()

        # 2. Define the personality and website rules for your AI
        system_instruction = (
            "You are the official AI Assistant for the Digital Library platform. "
            "Your job is to help users navigate the website and answer book-related questions.\n\n"
            
            "WEBSITE NAVIGATION RULES:\n"
            "- To BORROW a book: Tell the user to search for the book on the platform and click the 'Borrow' button.\n"
            "- To RETURN a book: Tell the user to go to their personal dashboard and click 'Return' next to the book.\n"
            "- To REGISTER/SIGN UP: Tell them to go to the Registration page, fill out the details, and verify their email.\n"
            "- To FIND books: Tell them to use the main search bar on the homepage.\n\n"
            
            "BOOK KNOWLEDGE RULES:\n"
            "- If a user asks about *any* book, author, or literary plot, answer them thoroughly and sincerely using your general knowledge, "
            "even if that book isn't explicitly on this website.\n"
            "- Keep your tone helpful, welcoming, professional, and friendly."
        )

        # 3. Call the Gemini model (gemini-2.5-flash is perfect for fast chat responses)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=500,
                temperature=0.7, # Balanced creativity for book discussions
            )
        )
        
        return response.text

    except Exception as e:
        # Fallback in case the API key is missing, expires, or there's a network issue
        print(f"Gemini API Error: {e}")
        return "I'm having trouble connecting to my brain right now. For website help: you can borrow books from their detail page or return them from your dashboard!"