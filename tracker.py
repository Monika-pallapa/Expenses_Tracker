import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import json

FILENAME = "expenses.json"

# -----------------------------
# Data Handling
# -----------------------------
def load_expenses():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


expenses = load_expenses()


def save_expenses():
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1050x680")
root.minsize(900, 600)
root.configure(bg="#f4f6fb")


# -----------------------------
# Styling
# -----------------------------
BG = "#f4f6fb"
WHITE = "#ffffff"
DARK = "#202535"
MUTED = "#707789"
ACCENT = "#5b5bd6"
ACCENT_DARK = "#4747b8"
GREEN = "#2e9d68"
RED = "#d9534f"
BORDER = "#e2e5ec"

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=DARK,
    rowheight=38,
    fieldbackground=WHITE,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#eef0f7",
    foreground=DARK,
    font=("Segoe UI Semibold", 10),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#dedfff")],
    foreground=[("selected", DARK)]
)

# -----------------------------
# Header
# -----------------------------
header = tk.Frame(root, bg=WHITE, height=78)
header.pack(fill="x")
header.pack_propagate(False)

title_frame = tk.Frame(header, bg=WHITE)
title_frame.pack(side="left", padx=28, pady=13)

tk.Label(
    title_frame,
    text="Personal Expense Tracker",
    font=("Segoe UI Semibold", 22),
    bg=WHITE,
    fg=DARK
).pack(anchor="w")

tk.Label(
    title_frame,
    text="Track your spending. Stay in control.",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w")


# -----------------------------
# Content
# -----------------------------
content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=24, pady=20)


# -----------------------------
# Dashboard Cards
# -----------------------------
cards_frame = tk.Frame(content, bg=BG)
cards_frame.pack(fill="x", pady=(0, 18))

def create_card(parent, title, value, accent):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=6)

    tk.Frame(card, bg=accent, width=5).pack(side="left", fill="y")

    inner = tk.Frame(card, bg=WHITE)
    inner.pack(fill="both", expand=True, padx=18, pady=14)

    tk.Label(
        inner,
        text=title,
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    value_label = tk.Label(
        inner,
        text=value,
        font=("Segoe UI Semibold", 20),
        bg=WHITE,
        fg=DARK
    )
    value_label.pack(anchor="w", pady=(4, 0))

    return value_label


total_label = create_card(cards_frame, "Total Spending", "₹0.00", ACCENT)
count_label = create_card(cards_frame, "Total Expenses", "0", GREEN)
highest_label = create_card(cards_frame, "Highest Expense", "₹0.00", RED)
category_label = create_card(cards_frame, "Top Category", "-", "#e09b32")


# -----------------------------
# Toolbar
# -----------------------------
toolbar = tk.Frame(content, bg=BG)
toolbar.pack(fill="x", pady=(0, 12))

search_var = tk.StringVar()

search_box = tk.Entry(
    toolbar,
    textvariable=search_var,
    font=("Segoe UI", 10),
    relief="flat",
    bg=WHITE,
    fg=DARK,
    highlightbackground=BORDER,
    highlightthickness=1
)
search_box.pack(side="left", ipady=9, padx=(0, 8), fill="x", expand=True)

search_box.insert(0, "Search expense or category...")

def clear_search_placeholder(event):
    if search_box.get() == "Search expense or category...":
        search_box.delete(0, "end")

def restore_search_placeholder(event):
    if search_box.get().strip() == "":
        search_box.insert(0, "Search expense or category...")

search_box.bind("<FocusIn>", clear_search_placeholder)
search_box.bind("<FocusOut>", restore_search_placeholder)


def styled_button(parent, text, command, bg=ACCENT):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI Semibold", 10),
        bg=bg,
        fg=WHITE,
        activebackground=ACCENT_DARK,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        padx=18,
        pady=9,
        cursor="hand2"
    )


# -----------------------------
# Expense Table
# -----------------------------
table_frame = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_frame.pack(fill="both", expand=True)

columns = ("date", "expense", "category", "amount")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

tree.heading("date", text="DATE")
tree.heading("expense", text="EXPENSE")
tree.heading("category", text="CATEGORY")
tree.heading("amount", text="AMOUNT")

tree.column("date", width=150, anchor="center")
tree.column("expense", width=360, anchor="w")
tree.column("category", width=180, anchor="center")
tree.column("amount", width=180, anchor="e")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y", pady=10)


# -----------------------------
# Dashboard Update
# -----------------------------
def update_dashboard():
    if not expenses:
        total_label.config(text="₹0.00")
        count_label.config(text="0")
        highest_label.config(text="₹0.00")
        category_label.config(text="-")
        return

    total = sum(item["amount"] for item in expenses)
    highest = max(item["amount"] for item in expenses)

    category_total = {}

    for item in expenses:
        category = item["category"]
        category_total[category] = category_total.get(category, 0) + item["amount"]

    top_category = max(category_total, key=category_total.get)

    total_label.config(text=f"₹{total:.2f}")
    count_label.config(text=str(len(expenses)))
    highest_label.config(text=f"₹{highest:.2f}")
    category_label.config(text=top_category)


# -----------------------------
# Display Expenses
# -----------------------------
def display_expenses(items=None):
    for row in tree.get_children():
        tree.delete(row)

    if items is None:
        items = expenses

    for index, item in enumerate(items):
        tree.insert(
            "",
            "end",
            iid=str(index),
            values=(
                item["date"],
                item["expense"],
                item["category"],
                f"₹{item['amount']:.2f}"
            )
        )

    update_dashboard()


# -----------------------------
# Search
# -----------------------------
def search_expenses(*args):
    text = search_var.get().strip().lower()

    if text == "" or text == "search expense or category...":
        display_expenses()
        return

    filtered = []

    for item in expenses:
        if (
            text in item["expense"].lower()
            or text in item["category"].lower()
        ):
            filtered.append(item)

    for row in tree.get_children():
        tree.delete(row)

    for index, item in enumerate(filtered):
        tree.insert(
            "",
            "end",
            iid=str(index),
            values=(
                item["date"],
                item["expense"],
                item["category"],
                f"₹{item['amount']:.2f}"
            )
        )

    if not filtered:
        messagebox.showinfo("Search", "No matching expenses found.")


search_var.trace_add("write", search_expenses)


# -----------------------------
# Add Expense Window
# -----------------------------
def add_expense():
    window = tk.Toplevel(root)
    window.title("Add Expense")
    window.geometry("430x430")
    window.resizable(False, False)
    window.configure(bg=WHITE)
    window.grab_set()

    tk.Label(
        window,
        text="Add New Expense",
        font=("Segoe UI Semibold", 20),
        bg=WHITE,
        fg=DARK
    ).pack(pady=(25, 5))

    tk.Label(
        window,
        text="Enter the details below",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(pady=(0, 20))

    form = tk.Frame(window, bg=WHITE)
    form.pack(fill="x", padx=35)

    tk.Label(
        form,
        text="Expense Name",
        font=("Segoe UI Semibold", 10),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    expense_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        relief="flat",
        bg="#f5f6fa",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    expense_entry.pack(fill="x", ipady=9, pady=(5, 15))

    tk.Label(
        form,
        text="Amount",
        font=("Segoe UI Semibold", 10),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    amount_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        relief="flat",
        bg="#f5f6fa",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    amount_entry.pack(fill="x", ipady=9, pady=(5, 15))

    tk.Label(
        form,
        text="Category",
        font=("Segoe UI Semibold", 10),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    category_var = tk.StringVar(value="Food")

    category_box = ttk.Combobox(
        form,
        textvariable=category_var,
        values=["Food", "Travel", "Shopping", "Bills", "Other"],
        state="readonly",
        font=("Segoe UI", 10)
    )
    category_box.pack(fill="x", ipady=6, pady=(5, 20))

    def save_new_expense():
        name = expense_entry.get().strip()
        amount_text = amount_entry.get().strip()

        if not name:
            messagebox.showerror("Invalid Input", "Please enter an expense name.")
            return

        try:
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount greater than zero."
            )
            return

        expenses.append({
            "expense": name,
            "amount": amount,
            "category": category_var.get(),
            "date": str(date.today())
        })

        save_expenses()
        display_expenses()
        window.destroy()

    styled_button(
        window,
        "Add Expense",
        save_new_expense
    ).pack(pady=5)

    expense_entry.focus()


# -----------------------------
# Edit Expense
# -----------------------------
def edit_expense():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Select Expense",
            "Please select an expense from the table first."
        )
        return

    try:
        index = int(selected[0])
        item = expenses[index]
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to select this expense.")
        return

    window = tk.Toplevel(root)
    window.title("Edit Expense")
    window.geometry("430x430")
    window.resizable(False, False)
    window.configure(bg=WHITE)
    window.grab_set()

    tk.Label(
        window,
        text="Edit Expense",
        font=("Segoe UI Semibold", 20),
        bg=WHITE,
        fg=DARK
    ).pack(pady=(25, 20))

    form = tk.Frame(window, bg=WHITE)
    form.pack(fill="x", padx=35)

    tk.Label(
        form,
        text="Expense Name",
        font=("Segoe UI Semibold", 10),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    expense_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        relief="flat",
        bg="#f5f6fa",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    expense_entry.pack(fill="x", ipady=9, pady=(5, 15))
    expense_entry.insert(0, item["expense"])

    tk.Label(
        form,
        text="Amount",
        font=("Segoe UI Semibold", 10),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    amount_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        relief="flat",
        bg="#f5f6fa",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    amount_entry.pack(fill="x", ipady=9, pady=(5, 15))
    amount_entry.insert(0, str(item["amount"]))

    tk.Label(
        form,
        text="Category",
        font=("Segoe UI Semibold", 10),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    category_var = tk.StringVar(value=item["category"])

    category_box = ttk.Combobox(
        form,
        textvariable=category_var,
        values=["Food", "Travel", "Shopping", "Bills", "Other"],
        state="readonly",
        font=("Segoe UI", 10)
    )
    category_box.pack(fill="x", ipady=6, pady=(5, 20))

    def save_changes():
        name = expense_entry.get().strip()

        try:
            amount = float(amount_entry.get().strip())

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount greater than zero."
            )
            return

        if not name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an expense name."
            )
            return

        item["expense"] = name
        item["amount"] = amount
        item["category"] = category_var.get()

        save_expenses()
        display_expenses()
        window.destroy()

    styled_button(
        window,
        "Save Changes",
        save_changes
    ).pack(pady=5)


# -----------------------------
# Delete Expense
# -----------------------------
def delete_expense():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Select Expense",
            "Please select an expense from the table first."
        )
        return

    try:
        index = int(selected[0])
        item = expenses[index]
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to select this expense.")
        return

    confirm = messagebox.askyesno(
        "Delete Expense",
        f"Delete '{item['expense']}' for ₹{item['amount']:.2f}?"
    )

    if confirm:
        expenses.pop(index)
        save_expenses()
        display_expenses()


# -----------------------------
# Buttons
# -----------------------------
button_frame = tk.Frame(content, bg=BG)
button_frame.pack(fill="x", pady=(14, 0))

styled_button(
    button_frame,
    "+ Add Expense",
    add_expense
).pack(side="left", padx=(0, 8))

styled_button(
    button_frame,
    "Edit",
    edit_expense,
    bg="#3d7fc1"
).pack(side="left", padx=8)

styled_button(
    button_frame,
    "Delete",
    delete_expense,
    bg=RED
).pack(side="left", padx=8)

styled_button(
    button_frame,
    "Refresh",
    display_expenses,
    bg="#6d7484"
).pack(side="left", padx=8)


# -----------------------------
# Start Application
# -----------------------------
display_expenses()

root.mainloop()
