from tkinter import ttk

from database import Database
from .create_game import CreateGameWindow
from .update_game import UpdateGameWindow
from .delete_game import DeleteGameWindow


class GameCRUDFrame(ttk.Frame):
    db: Database

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        ttk.Label(self, text="Manage Games", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self, text="Add Game", command=self._add_game).pack(pady=5)
        ttk.Button(self, text="Update Game", command=self._update_game).pack(pady=5)
        ttk.Button(self, text="Delete Game", command=self._delete_game).pack(pady=5)

    def _add_game(self):
        CreateGameWindow(self, self.db)

    def _update_game(self):
        UpdateGameWindow(self, self.db)

    def _delete_game(self):
        DeleteGameWindow(self, self.db)
