import tkinter as tk
from tkinter import ttk, messagebox
from database import Database


class UpdateCategoryWindow(tk.Toplevel):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Update Category")
        self.geometry("300x200")

        # Select Category
        ttk.Label(self, text="Select Category").pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self, textvariable=self.category_var)
        self.category_combobox.pack(pady=5)
        self._populate_categories()

        # Name Entry
        ttk.Label(self, text="New Name").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        # Update Button
        ttk.Button(self, text="Update", command=self._update_in_db).pack(pady=10)

    def _populate_categories(self):
        categories = self.db.get_all_cognitive_categories()
        self.category_combobox["values"] = [category.name for category in categories]

    def _update_in_db(self):
        selected_name = self.category_var.get()
        new_name = self.name_entry.get().strip()

        if not selected_name or not new_name:
            messagebox.showerror("Error", "Both fields must be filled!")
            return

        category = self.db.get_cognitive_category(category_name=selected_name)
        category.name = new_name

        try:
            self.db.update_cognitive_category(category)
            messagebox.showinfo("Success", "Category updated successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
