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
            book = Book.from_api(info)
            books.append(book)

        return books
    else:
        print("Error:", response.status_code)
        return []
