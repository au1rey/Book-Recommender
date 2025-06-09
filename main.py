from flask import Flask, render_template, request, redirect, url_for
from app.fetch_books import fetch_books_by_query

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    books = []
    if request.method == 'POST':
        query = request.form['query']
        books = fetch_books_by_query(query)
    return render_template('home.html', books=books)

@app.route('/base')
def base():
    render_template('base.html')

@app.route('/recme')
def rec_me():
    render_template('recme.html')

@app.route('/profile')
def profile():
    render_template('profile.html')

@app.route('/library')
def library():
    render_template("library.html")

@app.route('/shelf/<shelfname>')
def display_shelf(shelf_name):
    all_shelves = {
        "read": [],
        "to read": [],
        "in progress": []
    }

    books = all_shelves.get(shelf_name.lower(), [])
    return render_template("shelf.html", shelf_name=shelf_name.title(), books=books)

if __name__ == "__main__":
    app.run(debug=True)
