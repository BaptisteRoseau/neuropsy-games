import tkinter as tk
import tkinter.ttk as ttk


class ConfirmWindow(tk.Toplevel):
    def __init__(self, parent, message="Are you sure?"):
        super().__init__(parent)
        self.result = None
        self.title("Confirmation")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # Block interaction with the parent window

        # Center the window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Message
        ttk.Label(self, text=message, anchor="center").pack(pady=20)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Yes", command=self._on_yes).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="No", command=self._on_no).pack(side=tk.LEFT, padx=10)

        self.protocol("WM_DELETE_WINDOW", self._on_no)  # Handle window close

    def _on_yes(self):
        self.result = True
        self.destroy()

    def _on_no(self):
        self.result = False
        self.destroy()

    def show(self):
        self.wait_window()  # Wait until the window is closed
        return self.result
