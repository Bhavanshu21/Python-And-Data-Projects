import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

FILENAME = "expenses.csv"

# Initialize CSV file
def initialize_file():
    try:
        with open(FILENAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])
    except FileExistsError:
        pass

# Add a new expense
def add_expense():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    category = input("Enter category (e.g. Food, Transport, Utilities): ")
    amount = input("Enter amount: ")
    note = input("Optional note: ")

    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])
    print("✅ Expense added!")

# View all expenses
def view_expenses():
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(" | ".join(row))
    except FileNotFoundError:
        print("No expenses found yet.")

# View monthly summary
def view_summary():
    summary = defaultdict(float)
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if len(row) < 3:
                    continue
                category = row[1]
                try:
                    amount = float(row[2])
                    summary[category] += amount
                except ValueError:
                    continue

        print("\n--- Monthly Summary by Category ---")
        for cat, total in summary.items():
            print(f"{cat}: ₹{total:.2f}")

        show_chart(summary)

    except FileNotFoundError:
        print("No expenses found yet.")

# Show bar chart
def show_chart(summary):
    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts, color='skyblue')
    plt.title('Expense Summary by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount (₹)')
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# Main menu
def main():
    initialize_file()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Monthly Summary")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            view_summary()
        elif choice == '4':
            print("Exiting tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# This script is a simple personal expense tracker that allows users to add expenses,