import tkinter as tk
from tkinter import ttk, messagebox
from models import CognitiveFunction
from database import Database

class AddFunctionWindow(tk.Toplevel):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Add Function")
        self.geometry("300x150")

        # Name Entry
        ttk.Label(self, text="Function Name").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        # Add Button
        ttk.Button(self, text="Add", command=self._add_to_db).pack(pady=10)

    def _add_to_db(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Function name cannot be empty!")
            return

        function = CognitiveFunction(name=name)
        try:
            self.db.add_cognitive_function(function)
            messagebox.showinfo("Success", "Function added successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
