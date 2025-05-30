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

if __name__ == "__main__":
    app.run(debug=True)
