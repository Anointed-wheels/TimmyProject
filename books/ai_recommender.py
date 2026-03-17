from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from books.models import Book


def get_book_recommendations(book_id, num=5):

    books = Book.objects.all()

    titles = []
    descriptions = []
    ids = []

    for book in books:
        titles.append(book.title)
        descriptions.append(book.description if book.description else "")
        ids.append(book.id)

    vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vectorizer.fit_transform(descriptions)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    try:
        index = ids.index(book_id)
    except ValueError:
        return []

    similarity_scores = list(enumerate(cosine_sim[index]))

    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similarity_scores = similarity_scores[1:num+1]

    recommended_ids = [ids[i[0]] for i in similarity_scores]

    return Book.objects.filter(id__in=recommended_ids)