import tkinter as tk
from tkinter import ttk
from models import CognitiveCategory
from ui.category.add_category import AddCategoryWindow
from ui.category.update_category import UpdateCategoryWindow
from ui.category.delete_category import DeleteCategoryWindow

class CategoryCRUDFrame(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        # Title
        ttk.Label(self, text="Manage Categories", font=("Arial", 16)).pack(pady=10)

        # Add Category Button
        ttk.Button(self, text="Add Category", command=self._add_category).pack(pady=5)

        # Update Category Button
        ttk.Button(self, text="Update Category", command=self._update_category).pack(pady=5)

        # Delete Category Button
        ttk.Button(self, text="Delete Category", command=self._delete_category).pack(pady=5)

    def _add_category(self):
        AddCategoryWindow(self, self.db)

    def _update_category(self):
        UpdateCategoryWindow(self, self.db)

    def _delete_category(self):
        DeleteCategoryWindow(self, self.db)
