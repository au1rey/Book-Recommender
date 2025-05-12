# app/fetch_books.py

import requests

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
            books.append({
                "title": info.get("title", "N/A"),
                "authors": info.get("authors", ["Unknown"]),
                "description": info.get("description", "No description."),
                "categories": info.get("categories", []),
                "rating": info.get("averageRating", "N/A"),
                "pageCount": info.get("pageCount", "N/A")
            })

        return books
    else:
        print("Error:", response.status_code)
        return []
