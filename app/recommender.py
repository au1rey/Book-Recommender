import requests
import random
from collections import Counter
from app.fetch_books import fetch_books_by_query, get_book_by_id

def getUserPreferences(user_library):
    categories = []
    authors = []
    for book in user_library:
        if book.categories:
            categories.extend(book.categories)
        if book.authors:
            authors.extend(book.authors)

    category_counts = Counter(categories)
    author_counts = Counter(authors)
    return category_counts, author_counts

def recommend_books(user_library):
    category_counts, author_counts = getUserPreferences(user_library)

    # Pick from favorite author or favorite category randomly
    query_pick = []
    if category_counts:
        top_categories = [cat for cat, count in category_counts.most_common(3)]
        query_pick.append(f"subject:{random.choice(top_categories)}")
    if author_counts:
        top_authors = [auth for auth, count in author_counts.most_common(3)]
        query_pick.append(f"inauthor:{random.choice(top_authors)}")

    # If no preferences, default to fiction
    query = random.choice(query_pick) if query_pick else "subject:fiction"

    # Get a list of existing ids and filter out books already in user's library
    existing_book_ids = {book.id for book in user_library}
    books = fetch_books_by_query(query, max_results=5)
    books = [book for book in books if book.id not in existing_book_ids]

    # Return top recommendation or None
    return books[0] if books else None
    
