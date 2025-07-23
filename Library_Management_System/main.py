# main.py
from library import Library # type: ignore

def admin_menu(library):
    """Displays the admin menu and handles admin actions."""
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Book")
        print("2. Add Member")
        print("3. List All Books")
        print("4. List All Members")
        print("5. Search Book")
        print("6. Exit to Main Menu")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)
        elif choice == '2':
            name = input("Enter member name: ")
            library.add_member(name)
        elif choice == '3':
            library.list_all_books()
        elif choice == '4':
            library.list_all_members()
        elif choice == '5':
            query = input("Enter title or author to search: ")
            library.search_book(query)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(library):
    """Displays the user menu and handles user actions."""
    while True:
        print("\n--- User Menu ---")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. Search Book")
        print("4. List All Available Books")
        print("5. Exit to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = int(input("Enter Book ID to issue: "))
            member_id = int(input("Enter your Member ID: "))
            library.issue_book(book_id, member_id)
        elif choice == '2':
            book_id = int(input("Enter Book ID to return: "))
            member_id = int(input("Enter your Member ID: "))
            library.return_book(book_id, member_id)
        elif choice == '3':
            query = input("Enter title or author to search: ")
            library.search_book(query)
        elif choice == '4':
            print("\n--- Available Books ---")
            for book in library.books.values():
                if not book.is_issued:
                    print(book)
            print("-----------------------")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    """The main function to run the library management system."""
    library = Library()
    
    # Simple password protection for admin
    ADMIN_PASSWORD = "admin" 

    while True:
        print("\nWelcome to the Library Management System")
        print("1. Admin Login")
        print("2. User Menu")
        print("3. Exit")
        
        main_choice = input("Enter your choice: ")

        if main_choice == '1':
            password = input("Enter admin password: ")
            if password == ADMIN_PASSWORD:
                admin_menu(library)
            else:
                print("Incorrect password.")
        elif main_choice == '2':
            user_menu(library)
        elif main_choice == '3':
            library.save_data()
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
