# database.py
import sqlite3

def connect_db():
    """Establishes a connection to the SQLite database and returns the connection and cursor."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    return conn, cursor

def initialize_db():
    """Creates the expenses and settings tables if they don't already exist."""
    conn, cursor = connect_db()
    # Create expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
    """)
    # Create settings table for theme persistence
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_expense(date, category, amount, description):
    """Adds a new expense record to the database."""
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    conn.close()

def get_expenses():
    """Retrieves all expense records from the database."""
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def delete_expense(expense_id):
    conn, cursor = connect_db()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def delete_all_expenses():
    conn, cursor = connect_db()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
# --- New functions for theme settings ---

def save_setting(key, value):
    """Saves a key-value setting to the database. Replaces existing key."""
    conn, cursor = connect_db()
    # Use REPLACE to either insert a new row or replace an existing one
    cursor.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def load_setting(key):
    """Loads a setting value by its key."""
    conn, cursor = connect_db()
    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
