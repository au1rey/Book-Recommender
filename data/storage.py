# Saving/Loading books to a json local storage file
import json

def save_books_to_file(books, filename="data/books.json"):
    with open("books.json", "w", encoding="utf-8") as f: # write into the file
        json.dump(books, f, indent=2)

def load_books_from_file(filename="data/books.json"):
    with open("books.json", "r", encoding="utf-8") as f:
        return json.load(f)