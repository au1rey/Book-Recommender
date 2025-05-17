# Test for loading and saving queries
# This is to test that my json logic is correct
import unittest
import os
from data.storage import save_books_to_file, load_books_from_file

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_books.json"
        self.sample_books = [ # Create a test book
            {
                "title": "A Game of Test",
                "authors": "George R. R. Martest",
                "description": "Testing is coming",
                "categories": ["Testing"],
                "rating": 4.5,
                "pageCount": 694
            }
        ]

    def test_save_and_load(self):
        # Save test book
        save_books_to_file(self.sample_books, "test_books.json")

        # Load test book
        loaded_testbooks = load_books_from_file("test_books.json")

        # Verify that they match
        self.assertEqual(self.sample_books, loaded_testbooks)

    def tearDown(self):
        # Clean up the test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
if __name__ == "__main__":
    unittest.main()