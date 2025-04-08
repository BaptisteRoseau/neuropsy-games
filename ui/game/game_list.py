import tkinter as tk
from tkinter import ttk
from ui.game.game_detail import GameDetailFrame
from database import Database


class GameListFrame(ttk.Frame):
    db: Database

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db

        # Title
        ttk.Label(self, text="Game List", font=("Arial", 16)).pack(pady=10)

        # Scrollable container for GameDetailFrames
        self.canvas = tk.Canvas(self)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

    def update_games(self, games):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Populate the scrollable frame with new GameDetailFrames
        for game in games:
            GameDetailFrame(self.scrollable_frame, game).pack(fill=tk.X, pady=5)
