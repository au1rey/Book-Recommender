import unittest
from app.fetch_books import fetch_books_by_query

class TestFetchBooks(unittest.TestCase):

    def test_fetch_books_by_query(self):
        query = "Fantasy"
        books = fetch_books_by_query(query)

        # Format the output for better readability
        print("Books fetched:")
        for book in books:
            print(f"Title: {book['title']}")
            print(f"Authors: {', '.join(book['authors'])}")
            print(f"Description: {book['description']}")
            print(f"Categories: {', '.join(book['categories'])}")
            print(f"Rating: {book['rating']}")
            print(f"Page Count: {book['pageCount']}")
            print("-" * 50)  # Separator
        
        # Checks if list of books is empty
        self.assertGreater(len(books), 0)  

if __name__ == "__main__":
    unittest.main()
