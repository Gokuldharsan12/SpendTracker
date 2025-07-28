import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

DATA_FILE = "expenses.json"

# ======== Data Functions ========
def load_expenses():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get().strip()

        if not category:
            messagebox.showerror("Error", "Category cannot be empty.")
            return

        expense = {
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        expenses.append(expense)
        save_expenses(expenses)
        update_table()
        clear_inputs()
        messagebox.showinfo("Success", "Expense added successfully!")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def update_table():
    for row in tree.get_children():
        tree.delete(row)

    total = 0
    for exp in expenses:
        tree.insert("", "end", values=(f"₹{exp['amount']}", exp["category"], exp["date"]))
        total += exp['amount']

    total_label.config(text=f"Total Spent: ₹{total:.2f}")

def clear_inputs():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)

# ======== GUI Setup ========
root = tk.Tk()
root.title("💰 SpendTrack - Modern Expense Tracker")
root.geometry("700x500")
root.configure(bg="#f9f9f9")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#4CAF50", foreground="white")
style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

# ======== Heading ========
tk.Label(root, text="SpendTrack 💸", font=("Helvetica", 22, "bold"), fg="#333", bg="#f9f9f9").pack(pady=10)

# ======== Input Frame ========
input_frame = tk.Frame(root, bg="#f9f9f9")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Amount (₹)", font=("Helvetica", 12), bg="#f9f9f9").grid(row=0, column=0, padx=10, pady=5)
amount_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=20)
amount_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Category", font=("Helvetica", 12), bg="#f9f9f9").grid(row=1, column=0, padx=10, pady=5)
category_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=20)
category_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(input_frame, text="Add Expense", font=("Helvetica", 11, "bold"),
          bg="#4CAF50", fg="white", command=add_expense, width=20).grid(row=2, columnspan=2, pady=15)

# ======== Expense Table ========
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="x")

cols = ("Amount", "Category", "Date")
tree = ttk.Treeview(table_frame, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True)

# ======== Total Label ========
total_label = tk.Label(root, text="Total Spent: ₹0.00", font=("Helvetica", 14, "bold"), bg="#f9f9f9", fg="#333")
total_label.pack(pady=10)

# ======== Load Initial Data ========
expenses = load_expenses()
update_table()

root.mainloop()
