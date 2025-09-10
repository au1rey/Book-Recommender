from flask import Flask, render_template, request, redirect, url_for
from app.fetch_books import fetch_books_by_query, get_book_by_id
from app.recommender import recommend_books
from app.models.book import Book
from flask import jsonify
import requests
import json

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

# RECOMMENDER: Simple recommendation system based on user library
@app.route('/recme')
def rec_me():
    # Load shelves from JSON
    shelves = load_shelves()
    print("Loaded shelves:", shelves)

    # For ease of use, put all books in a single list
    user_library = []
    for shelf in shelves:
        for books_dict in shelf['books']:
            user_library.append(Book.from_dict(books_dict))
    print(f"User library has {len(user_library)} books.")

    book_to_show = recommend_books(user_library)
    return render_template('recme.html', book=book_to_show)

@app.route('/add_to_library/<book_id>', methods=['POST'])
def add_to_library(book_id):

    # Get info from API
    book = get_book_by_id(book_id) # Fetch book object
    if not book:
        return "Book not found", 404
    
    # Load current shelves
    shelves = load_shelves()

    # Add to "Want to Read" shelf by default
    for shelf in shelves:
        if shelf['name'].lower() == "want to read":
            shelf['books'].append(book.to_dict())

    save_shelves(shelves)
    # Refresh page
    return redirect(url_for('rec_me'))

@app.route('/new_rec', methods=['POST'])
def new_rec():
    shelves = load_shelves()
    user_library = []
    for shelf in shelves:
        for books_dict in shelf['books']:
            user_library.append(Book.from_dict(books_dict))
    book_to_show = recommend_books(user_library)
    return render_template('recme.html', book=book_to_show)

@app.route('/profile')
def profile():
    return render_template('profile.html')


# LIBRARY: Shelf initialization and management

@app.route('/library')
def library():
    shelves = load_shelves()  # load shelves from JSON
    return render_template("library.html", shelves=shelves)


SHELVES_FILE = 'shelves.json'

DEFAULT_SHELVES = [
    {"name": "Read", "books": []},
    {"name": "Currently Reading", "books": []},
    {"name": "Want to Read", "books": []}
]

def load_shelves():
    try:
        with open(SHELVES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_shelves(shelves):
    with open(SHELVES_FILE, 'w') as f:
        json.dump(shelves, f, indent=4)

@app.route('/add-shelf', methods=['POST'])
def add_shelf():
    data = request.get_json()
    new_shelf_name = data.get('shelf_name')

    print(f"Adding new shelf: {new_shelf_name}")
    shelves = load_shelves()
    shelves.append({'name': new_shelf_name, 'books': []})

    save_shelves(shelves)

    return jsonify({"success": True, "shelf_name": new_shelf_name})

@app.route('/delete-shelf', methods=['POST'])
def delete_shelf():
    data = request.get_json()
    shelf_name = data.get('shelf_name')
    
    shelves = load_shelves()
    shelves = [s for s in shelves if s['name'].lower() != shelf_name.lower()]
    save_shelves(shelves)
    
    return jsonify({"success": True, "deleted_shelf": shelf_name})

 # BOOK PAGE: Specific book card w/ info and add to shelf option
@app.route('/book/<string:book_id>')
def book_page(book_id):
    # Check if search result 
    book = book_map.get(book_id) 

    # If not in search results, check shelves
    if not book:
        shelves = load_shelves()
        for shelf in shelves:
            for b in shelf['books']:
                if b['id'] == book_id:
                    book = Book.from_dict(b)
                    break
            if book:
                break
    if not book:
        return "Book not found", 404
    # Load shelves from JSON
    shelves = load_shelves() 
    return render_template('book_page.html', book=book, book_id=book_id, shelves=shelves)

@app.route('/add-to-shelf', methods=['POST'])
def add_to_shelf():
    data = request.get_json()
    shelf = data.get("shelf")
    book_id = data.get("book_id")

    # Get full book object using API and check if valid
    book = get_book_by_id(book_id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404
    
    # Load shelves
    shelves = load_shelves()

    # Find the target shelf and add the book
    for s in shelves:
        if s['name'].lower() == shelf.lower():
            # Avoid duplicates
            if not any(b['id'] == book.id for b in s['books']):
                s['books'].append(book.to_dict())
            break
    else:
        return jsonify({"success": False, "message": "Shelf not found"}), 404
    
    # Save updated shelves
    save_shelves(shelves)

    return jsonify({"success": True, "shelf": shelf})

# SHELF DISPLAY:
@app.route('/shelf/<shelf_name>')
def display_shelf(shelf_name):
    shelves = load_shelves()
    books = []
    for s in shelves:
        if s['name'].lower() == shelf_name.lower():
            books = [Book.from_dict(b) for b in s['books']]
    for book in books:
        print(book.thumbnail)
    return render_template("shelf.html", shelf_name=shelf_name.title(), books=books)

if __name__ == "__main__":
    app.run(debug=True)
