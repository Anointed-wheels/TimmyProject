import os
from google import genai
from google.genai import types
from django.conf import settings

def library_ai_response(user_message):
    try:
        # 1. Initialize the client (automatically picks up GEMINI_API_KEY from environment)
        client = genai.Client()

        # 2. Define the personality, branding, and strict guardrails for Melo Library
        system_instruction = (
            "You are the official AI Assistant for Melo Library.\n\n"
            
            "CRITICAL BOUNDARY RULE:\n"
            "- You can ONLY answer questions related to books, authors, literature, reading, poetry, plots, "
            "or navigating the Melo Library website platform.\n"
            "- If a user asks about *anything* completely unrelated to books or the library platform (for example: "
            "coding, math equations, general web searches, recipes, personal advice, sports scores, or unrelated tools), "
            "you must politely refuse to answer. State that you are specialized exclusively in books and helping them navigate Melo Library.\n\n"

            "WEBSITE NAVIGATION RULES:\n"
            "- To BORROW a book: Tell the user to search for the book on Melo Library and click the 'Borrow' button on its details page.\n"
            "- To RETURN a book: Tell the user to go to their personal dashboard and click 'Return' next to the book.\n"
            "- To REGISTER/SIGN UP: Tell them to go to the Registration page, fill out the details, and verify their email.\n"
            "- To FIND books: Tell them to use the main search bar on the homepage of Melo Library.\n\n"
            
            "BOOK KNOWLEDGE RULES:\n"
            "- If a user asks about any book, author, or literary plot, answer them thoroughly, engagingly, and sincerely using your general knowledge, "
            "even if that book isn't explicitly hosted on this website yet.\n"
            "- Keep your tone helpful, welcoming, professional, and friendly. Always refer to the platform as Melo Library."
        )

        # 3. Call the Gemini model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=500,
                temperature=0.5, # Slightly lowered for stricter adherence to guardrails
            )
        )
        
        return response.text

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm having trouble connecting to my brain right now. For Melo Library help: you can borrow books from their detail page or return them from your dashboard!"