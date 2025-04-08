import tkinter as tk

from database import Database

from .create_game import CreateGameWindow
from tkinter import ttk, messagebox


class UpdateGameWindow(CreateGameWindow):
    db: Database

    def __init__(self, parent, db: Database):
        super().__init__(parent, db)
        self.title("Update Game")
        ttk.Label(self, text="Select Game").pack()
        self.game_var = tk.StringVar()
        self.game_combobox = ttk.Combobox(self, textvariable=self.game_var)
        self.game_combobox.pack()
        self._populate_games()

        # Update Button
        self.action_button.destroy()
        self.action_button = ttk.Button(
            self, text="Update", command=self._update_in_db
        )
        self.action_button.pack(pady=10)

    def _populate_games(self):
        games = self.db.get_all_games()
        self.game_combobox["values"] = [game.title for game in games]

    def _update_in_db(self):
        selected_game_title = self.game_var.get()
        if not selected_game_title:
            messagebox.showerror("Error", "No game selected!")
            return

        game = self._game_from_form()
        game.id = self.db.get_game(game_title=selected_game_title)[0].id

        try:
            self.db.update_game(game)
            messagebox.showinfo("Success", "Game updated successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
