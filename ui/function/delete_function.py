import tkinter as tk
from tkinter import ttk, messagebox
from database import Database


class DeleteFunctionWindow(tk.Toplevel):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Delete Function")
        self.geometry("300x150")

        # Select Function
        ttk.Label(self, text="Select Function").pack(pady=5)
        self.function_var = tk.StringVar()
        self.function_combobox = ttk.Combobox(self, textvariable=self.function_var)
        self.function_combobox.pack(pady=5)
        self._populate_functions()

        # Delete Button
        ttk.Button(self, text="Delete", command=self._delete_from_db).pack(pady=10)

    def _populate_functions(self):
        functions = self.db.get_all_cognitive_functions()
        self.function_combobox["values"] = [function.name for function in functions]

    def _delete_from_db(self):
        selected_name = self.function_var.get()
        if not selected_name:
            messagebox.showerror("Error", "No function selected!")
            return

        function = self.db.get_cognitive_function(function_name=selected_name)

        try:
            self.db.delete_cognitive_function(function.id)
            messagebox.showinfo("Success", "Function deleted successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
