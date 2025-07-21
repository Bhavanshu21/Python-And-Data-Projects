# ExpenseTracker/database.py

import sqlite3
from datetime import date

DB_NAME = "expense_tracker.db"

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    # Return rows as dictionaries for easier access by column name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the database and creates the 'expenses' table if it doesn't exist.
    This is safe to run every time the application starts.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date DATE NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_expense(expense_date: date, category: str, amount: float, note: str):
    """Adds a new expense record to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (expense_date, category, amount, note) VALUES (?, ?, ?, ?)",
        (expense_date, category, amount, note)
    )
    conn.commit()
    conn.close()

def get_expenses(year: int = None, month: int = None):
    """
    Retrieves expenses from the database.
    Can be filtered by year and month.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT id, expense_date, category, amount, note FROM expenses"
    params = []
    
    if year and month:
        query += " WHERE strftime('%Y-%m', expense_date) = ?"
        params.append(f"{year:04d}-{month:02d}")
    elif year:
        query += " WHERE strftime('%Y', expense_date) = ?"
        params.append(str(year))

    query += " ORDER BY expense_date DESC"
    
    cursor.execute(query, params)
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def delete_expense(expense_id: int):
    """Deletes an expense record by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    # Check if a row was actually deleted
    changes = conn.total_changes
    conn.close()
    return changes > 0

def get_summary_by_category(year: int, month: int):
    """
    Retrieves a summary of expenses grouped by category for a specific month and year.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE strftime('%Y-%m', expense_date) = ?
        GROUP BY category
        ORDER BY total DESC
    """
    params = (f"{year:04d}-{month:02d}",)
    cursor.execute(query, params)
    summary = cursor.fetchall()
    conn.close()
    return summary
