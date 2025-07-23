# Project-1

# 1. The Command-Line File Organizer 📁🔍
This repository contains two Python scripts for organizing files within a directory.

-----

## 📁 Simple File Organizer (`organize_files_simple.py` - first code block)

This script provides a straightforward way to organize files in a given directory based on their file extensions. Each unique file extension gets its own dedicated folder.

### Features:

  * **Extension-based Organization**: Files are moved into subdirectories named after their extensions (e.g., `PDF_Files`, `JPG_Files`).
  * **Automatic Folder Creation**: Creates new folders if they don't exist.
  * **Basic Error Handling**: Checks for valid directory paths and handles potential file movement errors.

### How to Use:

1.  Save the first code block as `organize_files_simple.py`.
2.  Run the script from your terminal:
    ```bash
    python organize_files_simple.py
    ```
3.  The script will prompt you to enter the path of the directory you want to organize.

-----

## 🗂️ Advanced Category-Based File Organizer (`organize_files_advanced.py` - second code block)

This is a more robust file organizer that categorizes files into predefined groups (e.g., "Images", "Documents", "Audio", "Video", "Archives", "Scripts", "Other") instead of just by extension. It also includes command-line argument support and a dry-run mode for testing.

### Features:

  * **Category-Based Organization**: Files are grouped into logical categories defined by common file extensions.
  * **Customizable Categories**: Easily modify the `CATEGORIES` dictionary to define your own file groups and extensions.
  * **Command-Line Interface**: Accepts the directory path and an optional dry-run flag as command-line arguments.
  * **Dry Run Mode**: Simulate the organization process without actually moving any files, allowing you to preview changes.
  * **Duplicate File Handling**: Automatically renames files if a file with the same name already exists in the destination folder (e.g., `document.pdf` becomes `document(1).pdf`).
  * **Error Handling**: Gracefully handles invalid paths and issues during file operations.

### How to Use:

1.  Save the second code block as `organize_files_advanced.py`.

2.  Run the script from your terminal.

      * **To perform an actual organization**:

        ```bash
        python organize_files_advanced.py /path/to/your/directory
        ```

        Replace `/path/to/your/directory` with the actual path you want to organize.

      * **To simulate the organization (dry run)**:

        ```bash
        python organize_files_advanced.py /path/to/your/directory --dry-run
        ```

        This will show you what actions would be taken without making any changes to your files.

-----

## Technologies Used

  * **Python**: The core programming language.
  * **`os` module**: For interacting with the operating system, like listing directories and creating folders.
  * **`shutil` module**: For high-level file operations, specifically moving files.
  * **`argparse` module**: (In the advanced script) For parsing command-line arguments.

-----

## Contributing

Feel free to fork this repository, suggest improvements, or open issues if you encounter any problems.




# 2. Personal Expense Tracker🧾
This repository contains a **Personal Expense Tracker** application built with Python's Tkinter for the graphical user interface and SQLite for data storage. It allows users to efficiently manage their daily expenses, track spending, and visualize financial data through interactive graphs.

-----

## Features

  * **Expense Management**: Easily add, view, and delete expense records with details like date, category, amount, and description.
  * **Persistent Storage**: All expense data and user settings (like theme preferences and monthly targets) are securely stored in a local SQLite database.
  * **Theming**: Toggle between light and dark themes for a personalized user experience.
  * **Search Functionality**: Filter expenses by category to quickly find specific transactions.
  * **Bulk Upload**: Import multiple expense records at once from a CSV file.
  * **Interactive Statistics**: Visualize spending patterns with dynamic bar and pie charts, grouped by category, date, or month. Users can also filter these statistics by a custom date range.
  * **Monthly Spending Target**: Set a monthly budget and receive alerts if expenses exceed the target.

-----

## Technologies Used

  * **Python**: The core programming language.
  * **Tkinter**: For creating the graphical user interface.
  * **SQLite3**: A lightweight, file-based database for data storage.
  * **Matplotlib**: Used for generating various statistical plots and charts.
  * **Pandas**: For efficient data manipulation and analysis, especially for preparing data for charting.
  * **tkcalendar**: For user-friendly date selection in the statistics view.

-----

## How to Run

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/expense-tracker.git
    cd expense-tracker
    ```
2.  **Install dependencies**:
    ```bash
    pip install tkcalendar matplotlib pandas
    ```
3.  **Run the application**:
    ```bash
    python app.py
    ```

-----

## Project Structure

  * `app.py`: The main application file containing the Tkinter GUI and all the functionalities.
  * `database.py`: Handles all interactions with the SQLite database, including creating tables, adding, retrieving, and deleting expenses, and managing settings.
  * `expenses.db`: The SQLite database file (will be created automatically upon first run).
  * `light_mode.png`, `dark_mode.png`: Icons for theme toggling (optional, the app provides a fallback text button if icons are not found).

-----

## Contributing

Feel free to fork the repository, open issues, or submit pull requests to improve the application.

# 3. Library Management System🔍📚

# Console-Based Library Management System

A robust and efficient console-based application built with Python to simulate a complete library system. This project demonstrates core software engineering principles through a clean, object-oriented design and modular structure. It features separate roles for administrators and users, persistent data storage, and essential library functionalities.

---

### Features

-   **Dual User Roles:**
    -   **Admin Module:** A password-protected interface (`password: admin`) for managing the library's inventory.
        -   Add new books and register new members.
        -   View comprehensive lists of all books and registered members.
    -   **User Module:** An open-access menu for members to interact with the library.
        -   Issue and return books.
        -   Search for books by title or author.
        -   View all available books.

-   **Book Management:**
    -   **Issuance & Returns:** Tracks the status of each book (Available/Issued) and links issued books to members.
    -   **Fine Calculation:** Automatically calculates fines for overdue books (e.g., books kept for more than 14 days).

-   **Data Handling:**
    -   **Persistent Storage:** All book and member data is automatically saved to `books.json` and `members.json` upon exiting the application, ensuring no data is lost between sessions.
    -   **Data Integrity:** The system loads existing data upon startup, maintaining the library's state.

-   **Search Functionality:**
    -   Allows both admins and users to quickly find books by searching for partial or full matches of a book's title or author.

---

### Skills Demonstrated

-   **Object-Oriented Programming (OOP):** The system is built around classes for `Book`, `Member`, and `Library`, showcasing principles like encapsulation and abstraction.
-   **Data Handling & Persistence:** Reading from and writing to JSON files for persistent data storage.
-   **Modular Code Structure:** The project is organized into three distinct files (`models.py`, `library.py`, `main.py`) for better readability, maintainability, and separation of concerns.
-   **User Authentication:** Implements a basic password-based authentication logic for the admin role.
-   **Console I/O:** Clean and intuitive command-line interface for seamless user interaction.
-   **Core Python Libraries:** Effective use of standard libraries like `datetime` for handling dates, `json` for data serialization, and `os` for path management.

---

### How to Run

1.  **Prerequisites:** Ensure you have Python 3.x installed on your system.
2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```
3.  **Run the Application:**
    Execute the `main.py` file from your terminal.
    ```bash
    python main.py
    ```
4.  **Interact with the Menu:**
    -   Follow the on-screen prompts to navigate between the Admin and User menus.
    -   The password for the Admin menu is `admin`.

