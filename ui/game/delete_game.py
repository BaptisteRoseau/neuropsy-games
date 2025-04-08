import tkinter as tk
from tkinter import ttk, messagebox

from database import Database

class DeleteGameWindow(tk.Toplevel):
    db: Database
        
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Delete Game")
        self.geometry("400x200")

        # Select Game
        ttk.Label(self, text="Select Game").pack()
        self.game_var = tk.StringVar()
        self.game_combobox = ttk.Combobox(self, textvariable=self.game_var)
        self.game_combobox.pack()
        self._populate_games()

        # Delete Button
        ttk.Button(self, text="Delete", command=self._delete_from_db).pack(pady=10)

    def _populate_games(self):
        games = self.db.get_all_games()
        self.game_combobox["values"] = [game.title for game in games]

    def _delete_from_db(self):
        selected_game_title = self.game_var.get()

        if not selected_game_title:
            messagebox.showerror("Error", "No game selected!")
            return

        game = self.db.get_game(game_title=selected_game_title)[0]

        try:
            self.db.delete_game(game.id)
            messagebox.showinfo("Success", "Game deleted successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
