import tkinter as tk
from tkinter import ttk
from models import CognitiveFunction
from ui.function.add_function import AddFunctionWindow
from ui.function.update_function import UpdateFunctionWindow
from ui.function.delete_function import DeleteFunctionWindow

class FunctionCRUDFrame(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        # Title
        ttk.Label(self, text="Manage Functions", font=("Arial", 16)).pack(pady=10)

        # Add Function Button
        ttk.Button(self, text="Add Function", command=self._add_function).pack(pady=5)

        # Update Function Button
        ttk.Button(self, text="Update Function", command=self._update_function).pack(pady=5)

        # Delete Function Button
        ttk.Button(self, text="Delete Function", command=self._delete_function).pack(pady=5)

    def _add_function(self):
        AddFunctionWindow(self, self.db)

    def _update_function(self):
        UpdateFunctionWindow(self, self.db)

    def _delete_function(self):
        DeleteFunctionWindow(self, self.db)
