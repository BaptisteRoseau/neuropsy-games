import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class DeleteCategoryWindow(tk.Toplevel):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Delete Category")
        self.geometry("300x150")

        # Select Category
        ttk.Label(self, text="Select Category").pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self, textvariable=self.category_var)
        self.category_combobox.pack(pady=5)
        self._populate_categories()

        # Delete Button
        ttk.Button(self, text="Delete", command=self._delete_from_db).pack(pady=10)

    def _populate_categories(self):
        categories = self.db.get_all_cognitive_categories()
        self.category_combobox["values"] = [category.name for category in categories]

    def _delete_from_db(self):
        selected_name = self.category_var.get()
        if not selected_name:
            messagebox.showerror("Error", "No category selected!")
            return

        category = self.db.get_cognitive_category(category_name=selected_name)[0]

        try:
            self.db.delete_cognitive_category(category.id)
            messagebox.showinfo("Success", "Category deleted successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
