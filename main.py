from flask import Flask, render_template, request, redirect, url_for
from app.fetch_books import fetch_books_by_query
from app.models.book import Book
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

book_map = {}
@app.route('/search', methods = ['GET', 'POST'])
def search():
    books = []
    if request.method == 'POST':
        query = request.form['query']
        books = fetch_books_by_query(query)
        for book in books:
            book_map[book.id] = book
    return render_template('search.html', books=books)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/recme')
def rec_me():
    return render_template('recme.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/library')
def library():
    return render_template("library.html")

@app.route('/shelf/<shelfname>')
def display_shelf(shelf_name):
    all_shelves = {
        "read": [],
        "to read": [],
        "in progress": []
    }

    books = all_shelves.get(shelf_name.lower(), [])
    return render_template("shelf.html", shelf_name=shelf_name.title(), books=books)

@app.route('/book/<string:book_id>')
def book_page(book_id):
    book = book_map.get(book_id) 
    if not book:
        return "Book not found", 404
    # Temp shelves
    shelves = ["Read", "Currently Reading", "Want to Read"]
    return render_template('book_page.html', book=book, book_id=book_id, shelves=shelves)

@app.route('/add-to-shelf', methods=['POST'])
def add_to_shelf():
    data = request.get_json()
    shelf = data.get("shelf")
    book_id = data.get("book_id")
    return jsonify({"success": True, "shelf": shelf})

if __name__ == "__main__":
    app.run(debug=True)
