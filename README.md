# Project

# 1. The Command-Line File Organizer 📁🔍

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
