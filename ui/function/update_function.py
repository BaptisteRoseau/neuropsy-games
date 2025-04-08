import tkinter as tk
from tkinter import ttk, messagebox
from models import CognitiveFunction
from database import Database

class UpdateFunctionWindow(tk.Toplevel):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Update Function")
        self.geometry("300x200")

        # Select Function
        ttk.Label(self, text="Select Function").pack(pady=5)
        self.function_var = tk.StringVar()
        self.function_combobox = ttk.Combobox(self, textvariable=self.function_var)
        self.function_combobox.pack(pady=5)
        self._populate_functions()

        # Name Entry
        ttk.Label(self, text="New Name").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        # Update Button
        ttk.Button(self, text="Update", command=self._update_in_db).pack(pady=10)

    def _populate_functions(self):
        functions = self.db.get_all_cognitive_functions()
        self.function_combobox["values"] = [function.name for function in functions]

    def _update_in_db(self):
        selected_name = self.function_var.get()
        new_name = self.name_entry.get().strip()

        if not selected_name or not new_name:
            messagebox.showerror("Error", "Both fields must be filled!")
            return

        function = self.db.get_cognitive_function(function_name=selected_name)[0]
        function.name = new_name

        try:
            self.db.update_cognitive_function(function)
            messagebox.showinfo("Success", "Function updated successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
