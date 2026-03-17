def library_ai_response(message):

    message = message.lower()

    if "borrow" in message:
        return "To borrow a book, search for the book and click the borrow button."

    elif "return" in message:
        return "To return a book, go to your dashboard and click return."

    elif "register" in message:
        return "You can register using the register page and verify your email."

    elif "book" in message:
        return "You can search for books using the search bar on the homepage."

    else:
        return "I am your Digital Library assistant. Ask me about borrowing, returning books or searching."