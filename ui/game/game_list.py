import tkinter as tk
from tkinter import ttk

from database import Database


class GameListFrame(ttk.Frame):
    db: Database

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db

        # Title
        ttk.Label(self, text="Game List", font=("Arial", 16)).pack(pady=10)

        # Listbox
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Populate listbox
        self._populate_list()

    def _populate_list(self):
        # Fetch games and populate the listbox
        games = self.db.get_all_games()
        for game in games:
            self.listbox.insert(tk.END, game.title)
