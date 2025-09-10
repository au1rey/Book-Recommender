# app/fetch_books.py
import requests
from app.models.book import Book


def fetch_books_by_query(query, max_results=5):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": max_results,
        "printType": "books"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        books = []

        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            book = Book.from_api(info, book_id=item.get("id"))
            books.append(book)

        return books
    else:
        print("Error:", response.status_code)
        return []

def get_book_by_id(book_id):
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        info = data.get("volumeInfo", {})
        return Book.from_api(info, book_id=data.get("id"))
    else:
        print("Error:", response.status_code)
        return None