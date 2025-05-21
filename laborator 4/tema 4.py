import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

DATA_FILE = "books.json"

class Book:
    def __init__(self, title, author, year, isbn, read=False):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.read = read

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "read": self.read
        }

    @staticmethod
    def from_dict(data):
        return Book(
            data["title"],
            data["author"],
            data["year"],
            data["isbn"],
            data.get("read", False)
        )

class BookDB:
    def __init__(self, filename):
        self.filename = filename
        self.books = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book.from_dict(b) for b in data]
        else:
            self.books = []

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def add_book(self, book):
        self.books.append(book)
        self.save()

    def update_book(self, index, book):
        self.books[index] = book
        self.save()

    def delete_book(self, index):
        del self.books[index]
        self.save()

class BookForm(tk.Toplevel):
    def __init__(self, master, on_save, book=None, index=None):
        super().__init__(master)
        self.title("Add / Edit Book")
        self.resizable(False, False)
        self.on_save = on_save
        self.book = book
        self.index = index
        self.create_widgets()
        self.grab_set()
        self.focus()
        if book:
            self.fill_form()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0)

        ttk.Label(frm, text="Title:").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(frm, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=0, column=1, pady=2)

        ttk.Label(frm, text="Author:").grid(row=1, column=0, sticky="w")
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(frm, textvariable=self.author_var, width=40)
        self.author_entry.grid(row=1, column=1, pady=2)

        ttk.Label(frm, text="Year:").grid(row=2, column=0, sticky="w")
        self.year_var = tk.StringVar()
        self.year_entry = ttk.Entry(frm, textvariable=self.year_var, width=40)
        self.year_entry.grid(row=2, column=1, pady=2)

        ttk.Label(frm, text="ISBN:").grid(row=3, column=0, sticky="w")
        self.isbn_var = tk.StringVar()
        self.isbn_entry = ttk.Entry(frm, textvariable=self.isbn_var, width=40)
        self.isbn_entry.grid(row=3, column=1, pady=2)

        self.read_var = tk.BooleanVar()
        self.read_check = ttk.Checkbutton(frm, text="Read", variable=self.read_var)
        self.read_check.grid(row=4, column=1, sticky="w", pady=5)

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.save_btn = ttk.Button(btn_frame, text="Save", command=self.save)
        self.save_btn.pack(side="left", padx=5)
        self.cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.destroy)
        self.cancel_btn.pack(side="left", padx=5)

    def fill_form(self):
        self.title_var.set(self.book.title)
        self.author_var.set(self.book.author)
        self.year_var.set(self.book.year)
        self.isbn_var.set(self.book.isbn)
        self.read_var.set(self.book.read)

    def save(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        year = self.year_var.get().strip()
        isbn = self.isbn_var.get().strip()
        read = self.read_var.get()

        if not title or not author or not year or not isbn:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not year.isdigit():
            messagebox.showerror("Error", "Year must be a number.")
            return

        book = Book(title, author, year, isbn, read)
        self.on_save(book, self.index)
        self.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Catalog")
        self.geometry("780x500")
        self.resizable(True, True)
        self.configure(bg="#F7A8B8")

        self.sort_reverse = {}
        self.db = BookDB(DATA_FILE)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white",
                        font=('Helvetica', 14), rowheight=30)
        style.map("Treeview", background=[('selected', '#A7C7E7')], foreground=[('selected', 'black')])
        style.configure("Treeview.Heading", background="#7BAFD4", foreground="white",
                        font=('Helvetica', 15, 'bold'))
        style.configure("TButton", background="#7BAFD4", foreground="white",
                        font=('Helvetica', 14, 'bold'), padding=8)
        style.map("TButton", background=[('active', '#A7C7E7')], foreground=[('active', 'black')])
        style.configure("TLabel", background="#F7A8B8", font=('Helvetica', 14))
        style.configure("TEntry", font=('Helvetica', 14))

        self.create_widgets()
        self.populate_books()

    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=(10, 0))

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.populate_books())
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=(0, 10))

        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Title", "Author", "Year", "ISBN", "Read")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.sort_reverse[col] = False
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            if col == "Title":
                self.tree.column(col, width=200, anchor="w")
            elif col == "Read":
                self.tree.column(col, width=70, anchor="center")
            else:
                self.tree.column(col, width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.add_btn = ttk.Button(btn_frame, text="Add Book", command=self.add_book)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ttk.Button(btn_frame, text="Edit Selected", command=self.edit_book)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete Selected", command=self.delete_book)
        self.delete_btn.pack(side="left", padx=5)

        self.toggle_read_btn = ttk.Button(btn_frame, text="Read", command=self.toggle_read_status)
        self.toggle_read_btn.pack(side="left", padx=5)

    def populate_books(self):
        query = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, book in enumerate(self.db.books):
            read_str = "Yes" if book.read else "No"
            values = (book.title, book.author, book.year, book.isbn, read_str)
            if query:
                joined = " ".join(str(v).lower() for v in values)
                if query not in joined:
                    continue
            self.tree.insert("", "end", iid=i, values=values)

    def sort_by_column(self, column):
        key_map = {
            "Title": lambda b: b.title.lower(),
            "Author": lambda b: b.author.lower(),
            "Year": lambda b: int(b.year),
            "ISBN": lambda b: b.isbn,
            "Read": lambda b: b.read
        }
        reverse = self.sort_reverse[column]
        self.db.books.sort(key=key_map[column], reverse=reverse)
        self.sort_reverse[column] = not reverse
        self.populate_books()

        arrow = " ↓" if reverse else " ↑"
        for col in self.tree["columns"]:
            heading = col + arrow if col == column else col
            self.tree.heading(col, text=heading, command=lambda c=col: self.sort_by_column(c))

    def add_book(self):
        BookForm(self, self.save_new_book)

    def save_new_book(self, book, index=None):
        self.db.add_book(book)
        self.populate_books()
        messagebox.showinfo("Success", "Book added successfully.")

    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a book to edit.")
            return
        index = int(selected[0])
        book = self.db.books[index]
        BookForm(self, self.save_edited_book, book, index)

    def save_edited_book(self, book, index):
        if index is None:
            return
        self.db.update_book(index, book)
        self.populate_books()
        messagebox.showinfo("Success", "Book updated successfully.")

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a book to delete.")
            return
        index = int(selected[0])
        book = self.db.books[index]
        answer = messagebox.askyesno("Confirm Delete", f"Delete '{book.title}' by {book.author}?")
        if answer:
            self.db.delete_book(index)
            self.populate_books()
            messagebox.showinfo("Deleted", "Book deleted successfully.")

    def toggle_read_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a book to toggle read status.")
            return
        index = int(selected[0])
        book = self.db.books[index]
        book.read = not book.read
        self.db.update_book(index, book)
        self.populate_books()

if __name__ == "__main__":
    app = App()
    app.mainloop()
