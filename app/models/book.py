# Structured Book Class Using API data
class Book:
    def __init__(self, title, authors, description, categories, rating, page_count, thumbnail=None):
        self.title = title
        self.authors = authors
        self.description = description
        self.categories = categories
        self.rating = rating
        self.page_count = page_count
        self.thumbnail = thumbnail
        # Custom attributes
        self.is_read = False 
        self.want_to_read = False
        self.user_rating = 0.0
        self.date_read = 0

    def mark_as_read(self):
        self.is_read = True
    
    def mark_as_want_to_read(self):
        self.want_to_read = True
    
    def to_dict(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "description": self.description,
            "categories": self.categories,
            "rating": self.rating,
            "pageCount": self.page_count,
            "isRead": self.is_read,
            "wantToRead": self.want_to_read,
            "userRating": self.user_rating,
            "dateRead": self.date_read
        }
    
    @classmethod
    def from_dict(cls, data): # Helps when loading from dictionary
        book = cls(
            title=data.get("title"),
            authors=data.get("authors"),
            description=data.get("description"),
            categories=data.get("categories"),
            rating=data.get("rating"),
            pageCount=data.get("pageCount")
        )


    @classmethod
    def from_api(cls, info):
        return cls(
            title=info.get("title", "N/A"),
            authors=info.get("authors", ["Unknown"]),
            description=info.get("description", "No description."),
            categories=info.get("categories", []),
            rating=info.get("averageRating", "N/A"),
            page_count=info.get("pageCount", "N/A"),
            thumbnail=info.get("imageLinks", {}).get("thumbnail")
        )