# models.py
import datetime

class Book:
    """Represents a single book in the library."""
    def __init__(self, title, author, book_id=None):
        self.book_id = book_id if book_id else id(self) # Use object id if no book_id is given
        self.title = title
        self.author = author
        self.is_issued = False

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"ID: {self.book_id} | Title: {self.title} | Author: {self.author} | Status: {status}"

class Member:
    """Represents a library member."""
    def __init__(self, name, member_id=None):
        self.member_id = member_id if member_id else id(self)
        self.name = name
        self.issued_books = {} # Using a dictionary to store issued date: {book_id: issue_date}

    def __str__(self):
        return f"ID: {self.member_id} | Name: {self.name} | Books Issued: {len(self.issued_books)}"

