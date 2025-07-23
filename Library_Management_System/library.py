# library.py
import datetime
from models import Book, Member # type: ignore
import json

class Library:
    """Manages all library operations."""
    def __init__(self, fine_per_day=1.0):
        self.books = {}
        self.members = {}
        self.fine_per_day = fine_per_day
        self.load_data()

    def add_book(self, title, author):
        """Adds a new book to the library."""
        book = Book(title, author)
        self.books[book.book_id] = book
        print(f"\n[Success] Book '{title}' added successfully.")

    def add_member(self, name):
        """Adds a new member to the library."""
        member = Member(name)
        self.members[member.member_id] = member
        print(f"\n[Success] Member '{name}' added successfully.")

    def issue_book(self, book_id, member_id):
        """Issues a book to a member."""
        book = self.books.get(book_id)
        member = self.members.get(member_id)

        if not book:
            print("\n[Error] Book not found.")
            return
        if not member:
            print("\n[Error] Member not found.")
            return
        if book.is_issued:
            print("\n[Error] Book is already issued.")
            return

        book.is_issued = True
        member.issued_books[book_id] = datetime.date.today()
        print(f"\n[Success] '{book.title}' issued to {member.name}.")

    def return_book(self, book_id, member_id):
        """Processes a returned book and calculates fine if any."""
        book = self.books.get(book_id)
        member = self.members.get(member_id)

        if not book:
            print("\n[Error] Book not found.")
            return
        if not member:
            print("\n[Error] Member not found.")
            return
        if book_id not in member.issued_books:
            print("\n[Error] This book was not issued to this member.")
            return

        issue_date = member.issued_books.pop(book_id)
        book.is_issued = False
        
        # Calculate fine (e.g., if returned after 14 days)
        days_issued = (datetime.date.today() - issue_date).days
        fine = 0
        if days_issued > 14:
            fine = (days_issued - 14) * self.fine_per_day
            print(f"\n[Fine] Book returned {days_issued - 14} days late. Fine: ₹{fine:.2f}")

        print(f"\n[Success] '{book.title}' has been returned.")

    def search_book(self, query):
        """Searches for books by title or author."""
        results = [
            book for book in self.books.values()
            if query.lower() in book.title.lower() or query.lower() in book.author.lower()
        ]
        if not results:
            print("\nNo books found matching your query.")
            return
        
        print("\n--- Search Results ---")
        for book in results:
            print(book)
        print("----------------------")

    def list_all_books(self):
        if not self.books:
            print("\nNo books in the library.")
            return
        print("\n--- All Books ---")
        for book in self.books.values():
            print(book)
        print("-----------------")
        
    def list_all_members(self):
        if not self.members:
            print("\nNo members in the library.")
            return
        print("\n--- All Members ---")
        for member in self.members.values():
            print(member)
        print("-------------------")

    def save_data(self):
        """Saves library data to JSON files."""
        # Convert book objects to dictionaries
        books_data = {bid: {"title": b.title, "author": b.author, "is_issued": b.is_issued} for bid, b in self.books.items()}
        with open("books.json", "w") as f:
            json.dump(books_data, f)

        # Convert member objects to dictionaries
        members_data = {mid: {"name": m.name, "issued_books": {bid: str(date) for bid, date in m.issued_books.items()}} for mid, m in self.members.items()}
        with open("members.json", "w") as f:
            json.dump(members_data, f)
        print("\n[System] Data saved successfully.")

    def load_data(self):
        """Loads library data from JSON files."""
        try:
            with open("books.json", "r") as f:
                books_data = json.load(f)
                for bid, b_data in books_data.items():
                    book = Book(b_data['title'], b_data['author'], int(bid))
                    book.is_issued = b_data['is_issued']
                    self.books[int(bid)] = book
        except (FileNotFoundError, json.JSONDecodeError):
            pass # No data to load

        try:
            with open("members.json", "r") as f:
                members_data = json.load(f)
                for mid, m_data in members_data.items():
                    member = Member(m_data['name'], int(mid))
                    member.issued_books = {int(bid): datetime.datetime.strptime(date_str, "%Y-%m-%d").date() for bid, date_str in m_data['issued_books'].items()}
                    self.members[int(mid)] = member
        except (FileNotFoundError, json.JSONDecodeError):
            pass # No data to load
